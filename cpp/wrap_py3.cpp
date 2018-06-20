#include "geodesic_distance.cpp"


static struct PyModuleDef cGeosDis =
{
    PyModuleDef_HEAD_INIT,
    "geodesic_distance", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    Methods
};


PyMODINIT_FUNC PyInit_geodesic_distance(void) {
    import_array();
    return PyModule_Create(&cGeosDis);
}
