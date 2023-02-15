def jxl_d(effort: int = 7):
    return {
        "name": f"jxl_e{effort}_d",
        "cmd": f"cjxl %IMG% -d %Q% -j 0 -e {effort} --patches=0 %OUT%",
        "ext": "jxl",
        "qualities": [0, 2],
    }


def avif10_q(speed: int = 4):
    return {
        "name": f"avif10_s{speed}_q",
        "cmd": f"avifenc %IMG% --min 1 --max 63 -d 10 -s {speed} -j 6"
        " -a end-usage=q -a cq-level=%Q%"
        " -a color:enable-chroma-deltaq=1 -a color:deltaq-mode=3  -a color:enable-qm=1"
        " -a color:enable-dnl-denoising=0 -a color:denoise-noise-level=5"
        " -a tune=ssim %OUT%",
        "ext": "avif",
        "qualities": [2, 26],
        "quality_integer_only": True,
    }


def avif8_q(speed: int = 4):
    return {
        "name": f"avif8_s{speed}_q",
        "cmd": f"avifenc %IMG% --min 1 --max 63 -d 8 -s {speed} -j 6"
        " -a end-usage=q -a cq-level=%Q%"
        " -a color:enable-chroma-deltaq=1 -a color:deltaq-mode=3 -a color:enable-qm=1"
        " -a color:enable-dnl-denoising=0 -a color:denoise-noise-level=5"
        " -a tune=butteraugli %OUT%",
        "ext": "avif",
        "qualities": [2, 26],
        "quality_integer_only": True,
    }


def cavif_q(speed: int = 4):
    return {
        "name": f"cavif_s{speed}_Q",
        "cmd": f"cavif -Q %Q% -s {speed} %IMG% -o %OUT% -f",
        "ext": "avif",
        "qualities": [82, 98],
        #
    }


def replace_dot(i: float | str):
    return str(i).replace(".", ",")
