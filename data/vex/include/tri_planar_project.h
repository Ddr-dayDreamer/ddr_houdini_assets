#ifndef __TRI_PLANAR_PROJECT__
#define __TRI_PLANAR_PROJECT__

#include <tri_planar_project.h>

function
float two_vector_angle(vector a;vector b){
    float up = dot(a, b);
    float down = length(a)*length(b);
    float angle = acos(up/down);
    angle = angle/PI*180;
    return angle;
}



// function
// vector tri_planar_project(
//     const vector pos;
//     const vector N;
// ){
//     vector uv = {0,0,0};
//     // test for normal dir
//     float angletox = two_vector_angle(N,{1,0,0});
//     if(angletox>90){
//         angletox = 180-angletox;
//     }

//     float angletoy = two_vector_angle(N,{0,1,0});
//     if(angletoy>90){
//         angletoy = 180-angletoy;
//     }

//     float angletoz = two_vector_angle(N,{0,0,1});
//     if(angletoz>90){
//         angletoz = 180-angletoz;
//     }


//     if(angletox<angletoy && angletox<angletoz){
//         uv.x = pos.z*-1;
//         uv.y = pos.y;
//         return uv;
//     }
//     if(angletoy<angletox && angletoy<angletoz){
//         uv.x = pos.x;
//         uv.y = pos.z*-1;
//         return uv;
//     }
//     else{
//         uv.x = pos.x;
//         uv.y = pos.y;
//         return uv;
//     }
// }

function
vector tri_planar_project(
    vector pos;
    vector N;
    float scale;
){
    vector uv = {0,0,0};
    // test for normal dir
    float angletox = two_vector_angle(N,{1,0,0});
    if(angletox>=90){
        angletox = 180-angletox;
    }

    float angletoy = two_vector_angle(N,{0,1,0});
    if(angletoy>=90){
        angletoy = 180-angletoy;
    }

    float angletoz = two_vector_angle(N,{0,0,1});
    if(angletoz>=90){
        angletoz = 180-angletoz;
    }


    if(angletox<=angletoy+0.001 && angletox<=angletoz+0.001){

        
        uv.x = pos.z*-1/scale;
        uv.y = pos.y/scale;
        return uv;
    }
    if(angletoy<=angletox+0.001 && angletoy<=angletoz+0.001){

        uv.x = pos.x/scale;
        uv.y = pos.z*-1/scale;
        return uv;
    }
    else{


        uv.x = pos.x/scale;
        uv.y = pos.y/scale;
        return uv;
    }
}



function
vector tri_planar_project(
    vector pos;
    vector N;
    float scale;
    int uv_no_backface;
){
    vector uv = {0,0,0};
    // test for normal dir
    float angletox = two_vector_angle(N,{1,0,0});
    if(angletox>=90){
        angletox = 180-angletox;
    }

    float angletoy = two_vector_angle(N,{0,1,0});
    if(angletoy>=90){
        angletoy = 180-angletoy;
    }

    float angletoz = two_vector_angle(N,{0,0,1});
    if(angletoz>=90){
        angletoz = 180-angletoz;
    }


    if(angletox<=angletoy+0.001 && angletox<=angletoz+0.001){

        if(uv_no_backface==1){
           if(N.x<0){
                pos.z *=-1;
            }
        }
        
        uv.x = pos.z*-1/scale;
        uv.y = pos.y/scale;
        return uv;
    }
    if(angletoy<=angletox+0.001 && angletoy<=angletoz+0.001){

        if(uv_no_backface==1){
           if(N.y<0){
                pos.x *=-1;
            }
        }

        uv.x = pos.x/scale;
        uv.y = pos.z*-1/scale;
        return uv;
    }
    else{

        if(uv_no_backface==1){
           if(N.z<0){
                pos.x *=-1;
            }
        }
        

        uv.x = pos.x/scale;
        uv.y = pos.y/scale;
        return uv;
    }
}




#endif