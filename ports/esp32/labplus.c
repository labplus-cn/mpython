#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/binary.h"
#include "modesp.h"

STATIC mp_obj_t labplus_init(void) {
    printf("init");
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(labplus_init_obj, labplus_init);



STATIC const mp_map_elem_t labplus_globals_table[] = {
	{ MP_OBJ_NEW_QSTR(MP_QSTR__name__), MP_OBJ_NEW_QSTR(MP_QSTR_labplus) },
	{ MP_OBJ_NEW_QSTR(MP_QSTR_init), (mp_obj_t)&labplus_init_obj }
};

STATIC MP_DEFINE_CONST_DICT(
	mp_module_labplus_globals,
	labplus_globals_table
);


const mp_obj_module_t mp_module_labplus = {
	.base = {&mp_type_module},
	.globals = (mp_obj_dict_t *)&mp_module_labplus_globals,
};
