#include "geodesic_distance.cpp"


static struct PyModuleDef cGeosDis =
{
    PyModuleDef_HEAD_INIT,
    "GeodisTK", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    Methods
};


PyMODINIT_FUNC PyInit_GeodisTK(void) {
    import_array();
    return PyModule_Create(&cGeosDis);
}
