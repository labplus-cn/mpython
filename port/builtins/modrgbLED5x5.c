// #include "image.h"
#include "rgb_display.h"
#include "image.h"
#include "py/obj.h"

STATIC const mp_rom_map_elem_t mpython_rgbLED5x5_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_Image),  MP_ROM_PTR(&machine_image_type) },
    { MP_ROM_QSTR(MP_QSTR_display), MP_ROM_PTR(&mpython_display_obj) },
};

STATIC MP_DEFINE_CONST_DICT(mpython_rgbLED5x5_locals_dict, mpython_rgbLED5x5_locals_dict_table);

const mp_obj_module_t mp_module_rgbLED5x5 = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_rgbLED5x5_locals_dict,
};