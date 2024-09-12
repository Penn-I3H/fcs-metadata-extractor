#include "Rcpp.h"
using namespace Rcpp;

// [[Rcpp::export]]
NumericMatrix js_matrix(NumericMatrix& probs) {
	int n = probs.ncol(), m=probs.nrow();
	NumericMatrix js_mat = NumericMatrix(n,n);
	NumericVector p, q, r;
	double js;

	for (int i=0; i<n-1; i++) {
		p = probs.column(i);

		for (int j=i+1; j<n; j++) {
			q = probs.column(j);
			r = (p+q)/2;
			js = 0;
			
			for (int k=0; k<m; k++) {
				if(p[k] > 0)
					js += p(k)*log2(p(k)/r(k));
				if(q[k] > 0)
					js += q(k)*log2(q(k)/r(k));
			}

			js_mat(i,j) = js/2;
			js_mat(j,i) = js/2;
		}
	}

	return js_mat;
}

