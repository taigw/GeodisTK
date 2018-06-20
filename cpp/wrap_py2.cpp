#include "geodesic_distance.cpp"

PyMODINIT_FUNC
initgeodesic_distance(void) {
    (void) Py_InitModule("geodesic_distance", Methods);
    import_array();
}
