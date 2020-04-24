#include <iostream>
#include <vector>
using namespace std;

struct Point2D
{
    float distance;
    int w;
    int h;
};

float get_l2_distance(std::vector<float> p1, std::vector<float> p2);

void geodesic2d_fast_marching(const float * img, const unsigned char * seeds, float * distance, 
    int height, int width, int channel);

void geodesic2d_raster_scan(const float * img, const unsigned char * seeds, float * distance,
	int height, int width, int channel, float lambda, int iteration);

