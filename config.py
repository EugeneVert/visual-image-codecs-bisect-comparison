def jxl_d(effort: int = 7):
    return {
        "name": f"jxl_e{effort}_d",
        "cmd": f"cjxl %IMG% -d %Q% -j 0 -e {effort} --patches=0 %OUT%",
        "ext": "jxl",
        "qualities": [0, 2],
    }


def avif_q(speed: int = 4):
    return {
        "name": f"avif_s{speed}_q",
        "cmd": f"avifenc %IMG% --min 0 --max 63 -d 10 -s {speed} -j 8"
        " -a end-usage=q -a cq-level=%Q%"
        " -a color:enable-chroma-deltaq=1 -a color:deltaq-mode=3"
        " -a color:aq-mode=1 -a color:qm-min=0 -a tune=ssim %OUT%",
        "ext": "avif",
        "qualities": [2, 50],
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
