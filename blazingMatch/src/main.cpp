#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

using namespace std;
namespace py = pybind11;

py::array_t<double> nearestScore(py::array_t<double> ctr_score, py::array_t<double> trt_score) {
  py::buffer_info buf0 = ctr_score.request();
  py::buffer_info buf1 = trt_score.request();

  int n0 = ctr_score.shape(0);
  int n1 = trt_score.shape(0);

  /*  allocate the buffer */
  py::array_t<double> result = py::array_t<double>(2*n1);
  py::buffer_info buf2 = result.request();

  double *ptr0 = (double *) buf0.ptr,
         *ptr1 = (double *) buf1.ptr,
         *ptr2 = (double *) buf2.ptr;

  int index0 = 0;
  int index1 = 0;

// row major implementation
//  while (index0 < n0 && index1 < n1) {
//    while (index0 + 1 < n0 && ptr0[2*(index0+1) + 1] < ptr1[2*index1 + 1]) {
//      index0++;
//    }
//    if (index0 + 1 == n0) {
//      for (int i=index1; i< n1; i++) {
//        ptr2[2*index1]     = ptr0[2*index0];
//        ptr2[2*index1 + 1] = ptr1[2*i];
//      }
//      break;
//    }
//    if (ptr0[2*(index0+1) + 1] - ptr1[2*index1 + 1] >= ptr1[2*index1 + 1] - ptr0[2*index0 + 1]) {
//      ptr2[2*index1]     = ptr0[2*index0];
//      ptr2[2*index1 + 1] = ptr1[2*index1];
//    } else {
//      ptr2[2*index1]     = ptr0[2*(index0+1)];
//      ptr2[2*index1 + 1] = ptr1[2*index1];
//      index0++;
//    }
//    index1++;
//  }

// column major implementation
  while (index0 < n0 && index1 < n1) {
    while (index0 + 1 < n0 && ptr0[n0+index0+1] < ptr1[n1+index1]) {
      index0++;
    }
    if (index0 + 1 == n0) {
      for (int i=index1; i< n1; i++) {
        ptr2[i]    = ptr0[index0];
        ptr2[n1+i] = ptr1[i];
      }
      break;
    }
    if (ptr0[n0+index0+1] - ptr1[n1+index1] >= ptr1[n1+index1] - ptr0[n0+index0]) {
      ptr2[index1]    = ptr0[index0];
      ptr2[n1+index1] = ptr1[index1];
    } else {
      ptr2[index1]    = ptr0[index0+1];
      ptr2[n1+index1] = ptr1[index1];
      index0++;
    }
    index1++;
  }

//  result.resize({n1, 2});
  return result;
}

PYBIND11_MODULE(cppmodule, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cppmodule

        .. autosummary::
           :toctree: _generate

           nearestScore
    )pbdoc";

    m.def("nearestScore", &nearestScore, R"pbdoc(
        generate nearest score index from control score and treatment score
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
