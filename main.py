from pathlib import Path
from multiprocessing import Pool, cpu_count
from subprocess import run, DEVNULL
from typing import Any
import shlex
import shutil
import bisect
import json


# class ImageSequenceGenerator:


class OptimalQualitySearch:
    cmd: list[str]
    ext: str
    image_path: Path
    name: str
    nproc: int
    output_dir: Path
    preview_dir: Path
    qualities: list[float]

    def __init__(
        self,
        settings: dict[str, Any],
        image_path: Path,
        output_dir: Path,
        preview_dir: Path,
        quality_steps: int = 8,
        nproc: int = cpu_count(),
    ):
        self.image_path = image_path
        self.output_dir = output_dir
        self.preview_dir = preview_dir

        if not ("%IMG%" in settings["cmd"] and "%OUT%" in settings["cmd"]):
            raise ValueError("No %IMG% or %OUT% prenet in cmd")

        self.cmd = shlex.split(settings["cmd"])
        self.ext = settings["ext"]
        self.name = settings["name"]
        self.nproc = nproc
        self.quality_integer_only = settings.get("quality_integer_only", False)

        qualities = settings["qualities"]
        quality_hi_to_low = settings.get("quality_hi_to_low", False)
        if quality_hi_to_low:
            min = qualities[1]
            max = qualities[0]
        else:
            min = qualities[0]
            max = qualities[1]
        step = (max - min) / quality_steps
        self.qualities = [min]
        for _ in range(quality_steps):
            self.qualities.append(self.qualities[-1] + step)

    def process(self) -> list[Path]:
        pool = Pool(self.nproc)
        res = pool.starmap(
            _process,
            (
                (self.cmd, self.image_path, self.output_dir, self.ext, quality)
                for quality in self.qualities
            ),
        )
        pool.close()
        return res

    def interactive_seach(self, pregenerated_images: list[Path]):
        # Copy original image to preview dir
        orig_path = self.preview_dir / f"orig{self.image_path.suffix}"
        shutil.copy2(self.image_path, orig_path)
        # Open default image viewer
        # run(["xdg-open", str(orig_path)], check=True)

        cmp_path = self.preview_dir / f"cmp.{self.ext}"
        # Pseudo Binary search for optimal quality
        left = self.qualities[0]
        right = self.qualities[-1]

        print("Please guide me! Decrease (<) or increase (>) setting?")
        prev_resp = ""
        while True:
            resp = ""
            if self.quality_integer_only:
                q = (left + right) // 2
            else:
                q = (left + right) / 2
            print(q)

            # Get encoded image
            index = bisect.bisect_left(self.qualities, q)
            if self.qualities[index] == q:
                img = pregenerated_images[index]
            else:
                img = _process(
                    self.cmd, self.image_path, self.output_dir, self.ext, q
                )
                self.qualities.insert(index, q)
                pregenerated_images.insert(index, img)
            shutil.copy2(img, cmp_path)

            # Parse input
            while resp not in (">", "<"):
                resp = input()
                if resp == "":
                    if prev_resp == "":
                        continue
                    resp = prev_resp
                if resp == "exit":
                    return (q, img)

            if resp == ">":
                left = q
            else:
                right = q
            prev_resp = resp

    def save_result(
        self,
        result_quality: float,
        result_image_path: Path,
        save_path: Path,
    ):
        output_path_orig = save_path / "origs"
        output_path_orig.mkdir(exist_ok=True)
        output_path_conv = save_path / self.name
        output_path_conv.mkdir(exist_ok=True)
        output_path_orig_image = output_path_orig / self.image_path.name

        if (
            not output_path_orig_image.exists()
            or output_path_orig_image.stat().st_size != self.image_path.stat().st_size
        ):
            shutil.copy2(self.image_path, output_path_orig_image)
        shutil.copy2(result_image_path, output_path_conv)

        output_path_data = save_path / "data.json"
        data = {}
        if output_path_data.exists():
            with open(output_path_data, "r") as f:
                data: dict[str, dict[str, Any]] = json.load(f)
        with open(output_path_data, "w") as f:
            info = data.setdefault(self.image_path.name, {})
            info[self.name] = {
                "cmd": self.cmd,
                "name": result_image_path.name,
                "quality": result_quality,
            }
            json.dump(data, f)

    def preview_cleanup(self):
        for i in self.preview_dir.glob("*"):
            i.unlink()


def _process(
    cmd_template: list[str],
    image_path: Path,
    output_dir: Path,
    output_ext: str,
    quality: float,
) -> Path:
    cmd: list[str] = []
    output_path = output_dir / f"{image_path.stem}_q{quality:.03f}.{output_ext}"
    for arg in cmd_template:
        if arg == "%IMG%":
            cmd.append(str(image_path))
        elif arg == "%OUT%":
            cmd.append(str(output_path))
        elif "%Q%" in arg:
            cmd.append(arg.replace("%Q%", f"{quality:g}"))
        else:
            cmd.append(arg)
    run(cmd, stderr=DEVNULL, stdout=DEVNULL, check=True)
    return output_path
