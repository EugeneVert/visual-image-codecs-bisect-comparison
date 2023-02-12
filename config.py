def jxl_d():
    return {
        "name": "jxl_d",
        "cmd": "cjxl %IMG% -d %Q% -j 0 -e 7 --patches=0 %OUT%",
        "ext": "jxl",
        "qualities": [0.1, 5],
    }


def avif_q():
    return {
        "name": "avif_q",
        "cmd": "avifenc %IMG% --min 0 --max 63 -d 10 -s 4 -j 8 -a end-usage=q -a cq-level=%Q% -a color:enable-chroma-deltaq=1 -a color:deltaq-mode=3 -a color:aq-mode=1 -a color:qm-min=0 -a tune=ssim %OUT%",
        "ext": "avif",
        "qualities": [2, 50],
        "quality_integer_only": True
    }


def cavif_q():
    return {
        "name": "cavif_Q",
        "cmd": "cavif -Q %Q% %IMG% -o %OUT%",
        "ext": "avif",
        "qualities": [40, 99],
        #
    }
