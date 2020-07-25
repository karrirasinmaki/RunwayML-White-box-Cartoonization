# =========================================================================

# RunwayML port of White-box-Cartoonization
# https://github.com/SystemErrorWang/White-box-Cartoonization
# https://www.runwayml.com

# =========================================================================

import runway
from runway.data_types import number, text, image
from cartoonize_model import CartoonizeModel

setup_options = {
    'model_path': text(description='Model path. Empty string = default model.'),
}
@runway.setup(options=setup_options)
def setup(opts):
    model = CartoonizeModel({
        'model_path': opts['model_path'] or 'WBCartoonization/test_code/saved_models'
    })
    return model

@runway.command(name='cartoonize',
        inputs={
            'image': image(),
            'resize': number(default=50, min=0, max=100, step=1)
        },
        outputs={
            'image': image()
        },
        description='Cartoonize.')
def cartoonize(model, args):
    output_image = model.cartoonize(args['image'], {
        'resize': args['resize'] / 100
    })
    return {
        'image': output_image
    }

if __name__ == '__main__':
    runway.run(host='0.0.0.0', port=8000)
