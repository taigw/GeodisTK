#include "geodesic_distance.cpp"

PyMODINIT_FUNC
initGeodisTK(void) {
    (void) Py_InitModule("GeodisTK", Methods);
    import_array();
}
