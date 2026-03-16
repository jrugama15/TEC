import os
import glob
import vtracer

def convert_to_svg(input_path, output_path):
    print(f"Tratando de vectorizar: {input_path}...")
    try:
        # vtracer paramters documentation: 
        # input (str) output (str) colormode (str: 'color' or 'binary')
        # We use strict default to be safe
        vtracer.convert_image_to_svg_py(
            input_path, 
            output_path,
            colormode="color",        # use "binary" to make it black & white
            hierarchical="stacked",   # "stacked" or "cutout"
            mode="spline",            # "spline", "polygon", or "none"
            filter_speckle=4,         # smooth small speckles
            color_precision=6,        # lower means fewer colors
            layer_difference=16,
            corner_threshold=60,
            length_threshold=4.0,
            max_iterations=10,
            splice_threshold=45,
            path_precision=8
        )
        print(f"Vectores extraídos en: {output_path}")
    except Exception as e:
        print(f"Error procesando {input_path}: {e}")

if __name__ == "__main__":
    src_dir = os.path.join(os.getcwd(), 'static', 'core', 'img')
    out_dir = os.path.join(os.getcwd(), 'iconos_svg')
    os.makedirs(out_dir, exist_ok=True)
    
    # Let's target pngs which are the logos, ignoring the big exact banner image
    # since vectorizing a banner photo will be a huge file and not really an icon
    files = glob.glob(os.path.join(src_dir, '*.png'))
    for f in files:
        basename = os.path.basename(f)
        out_f = os.path.join(out_dir, os.path.splitext(basename)[0] + '.svg')
        convert_to_svg(f, out_f)
    print("¡Terminado!")
