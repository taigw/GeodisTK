#include <iostream>
#include <vector>
#include <cmath>
#include <cstdio>
#include "util.h"
#include "fast_marching_distance2d.h"
using namespace std;

void insert_point_to_list(std::vector<Point2D> * list, int start_position,  Point2D p)
{
    int insert_idx = list->size();
    for(int i = start_position; i < list->size(); i++)
    {
        if(list->at(i).distance < p.distance)
        {
            insert_idx = i;
            break;
        }
    }
    list->insert(insert_idx + list->begin(), p);
}

void update_point_in_list(std::vector<Point2D> * list, Point2D p)
{
    int remove_idx = -1;
    for(int i = 0; i < list->size(); i++)
    {
        if(list->at(i).w == p.w && list->at(i).h == p.h)
        {
            remove_idx = i;
            break;
        }
    }
    list->erase(remove_idx + list->begin());
    insert_point_to_list(list, remove_idx, p);
}

void add_new_accepted_point(const float * img, float * distance, int * state, std::vector<Point2D> * list, int height, int width, Point2D p)
{
    int w = p.w;
    int h = p.h;
    int nh, nw, temp_state;
    float p_value, q_value;
    float p_dis, space_dis, delta_dis, old_dis, new_dis;
    p_value = get_pixel<float>(img, height, width, h, w);
    p_dis   = get_pixel<float>(distance, height, width, h, w);
    for(int dh = -1; dh <= 1; dh++)
    {
        for(int dw = -1; dw <= 1; dw++)
        {
            if(dh == 0 && dw == 0) continue;
            nh = dh + h;
            nw = dw + w;
            if(nh >=0 && nh < height && nw >=0 && nw < width)
            {
                temp_state = get_pixel<int>(state, height, width, nh, nw);
                if(temp_state == 0) continue;
                space_dis = sqrt(dw*dw + dh*dh);
                q_value   = get_pixel<float>(img, height, width, nh, nw);
                delta_dis = space_dis*abs(p_value - q_value);
                old_dis   = get_pixel<float>(distance, height, width, nh, nw);
                
                new_dis   = p_dis + delta_dis;
                if(new_dis < old_dis)
                {
                    set_pixel<float>(distance, height, width, nh, nw, new_dis);
                    Point2D new_point;
                    new_point.distance = new_dis;
                    new_point.h = nh;
                    new_point.w = nw;
                    if(temp_state == 2){
                        set_pixel<int>(state, height, width, nh, nw, 1);
                        insert_point_to_list(list, 0, new_point);
                    }
                    else{
                        update_point_in_list(list, new_point);
                    }
                }
            }
        } // end for dw
    } // end for dh
}

void geodesic_distance2d(const float * img, const unsigned char * seeds, float * distance, int height, int width)
{
    
    // point state: 0--acceptd, 1--temporary, 2--far away
    // get initial accepted set and far away set
    float init_dis;
    unsigned char seed_type;
    for(int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            seed_type = get_pixel<unsigned char>(seeds, height, width, h, w);
            init_dis = seed_type > 0 ? 0.0 : 1.0e10
            set_pixel<float>(distance, height, width, h, w, init_dis);
        }
    }
    
    // forward scann
    int dh_f[4] = {-1, -1, -1, 0};
    int dw_f[4] = {-1, 0, 1, -1};
    int local_dis_f[4] = {1.414, 1.0, 1.414, 1.0};
    // forward pass
    for(int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float p_dis = get_pixel<float>(distance, height, width, h, w);
            float p_value = get_pixel<float>(img, height, width, h, w);
            for(int i = 0; i < 4; i++)
            {
                int nh = h + dh_f[i];
                int nw = w + dw_f[i];
                if(nh < 0 || nh >= height || nw < 0 || nw >= width) continue;
                float q_dis = get_pixel<float>(distance, height, width, nh, nw);
                float q_value = get_pixel<float>(img, height, width, nh, nw);
                float delta_d = local_dis_f[i] * abs(p_value - q_value);
                float temp_dis = q_dis + delta_d;
                if(temp_dis < p_dis) p_dis = temp_dis;
            }
            set_pixel<float>(distance, height, width, nh, nw, p_dis);
        }
    }

    // backward scann
    int dh_b[4] = {0, 1, 1, 1};
    int dw_b[4] = {1, -1, 0, 1};
    int local_dis_b[4] = {1.0, 1.414, 1.0, 1.414};
    // forward pass
    for(int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float p_dis = get_pixel<float>(distance, height, width, h, w);
            float p_value = get_pixel<float>(img, height, width, h, w);
            for(int i = 0; i < 4; i++)
            {
                int nh = h + dh_b[i];
                int nw = w + dw_b[i];
                if(nh < 0 || nh >= height || nw < 0 || nw >= width) continue;
                float q_dis = get_pixel<float>(distance, height, width, nh, nw);
                float q_value = get_pixel<float>(img, height, width, nh, nw);
                float delta_d = local_dis_b[i] * abs(p_value - q_value);
                float temp_dis = q_dis + delta_d;
                if(temp_dis < p_dis) p_dis = temp_dis;
            }
            set_pixel<float>(distance, height, width, nh, nw, p_dis);
        }
    }
}