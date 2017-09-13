/*****************************************************************************
 *   Copyright (C) 2004-2015 The PaGMO development team,                     *
 *   Advanced Concepts Team (ACT), European Space Agency (ESA)               *
 *                                                                           *
 *   https://github.com/esa/pagmo                                            *
 *                                                                           *
 *   act@esa.int                                                             *
 *                                                                           *
 *   This program is free software; you can redistribute it and/or modify    *
 *   it under the terms of the GNU General Public License as published by    *
 *   the Free Software Foundation; either version 2 of the License, or       *
 *   (at your option) any later version.                                     *
 *                                                                           *
 *   This program is distributed in the hope that it will be useful,         *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of          *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           *
 *   GNU General Public License for more details.                            *
 *                                                                           *
 *   You should have received a copy of the GNU General Public License       *
 *   along with this program; if not, write to the                           *
 *   Free Software Foundation, Inc.,                                         *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.               *
 *****************************************************************************/

#include <algorithm>

#include "../config.h"
#include "../serialization.h"
#include "../population.h"
#include "../problem/tsp.h"
#include "base.h"
#include "nn_tsp.h"

namespace pagmo { namespace algorithm {
    
/// Constructor.
/**
 * Allows to specify in detail all the parameters of the algorithm.
 *
 * @param[in] start_city First City in the tour.
*/

nn_tsp::nn_tsp(int start_city) : base(),m_start_city(start_city)
{
}

    
/// Clone method.
base_ptr nn_tsp::clone() const
{
return base_ptr(new nn_tsp(*this));
}
    
/// Evolve implementation.
/**
 * Runs the NN_TSP algorithm.
 *
 * @param[in,out] pop input/output pagmo::population to be evolved.
 */
void nn_tsp::evolve(population &pop) const
{
	const problem::base_tsp* prob;
	//check if problem is of type pagmo::problem::base_tsp
	try
	{
	    prob = &dynamic_cast<const problem::base_tsp &>(pop.problem());
	}
	catch (const std::bad_cast& e)
	{
		pagmo_throw(value_error,"Problem not of type pagmo::problem::tsp, nn_tsp can only be called on problem::tsp problems");
	}

	// Let's store some useful variables.
	const problem::base::size_type Nv = prob->get_n_cities();

	//create individuals
	decision_vector best_tour(Nv);
	decision_vector new_tour(Nv);

	//check input parameter
	if (m_start_city < -1 || m_start_city > static_cast<int>(Nv-1)) {
		pagmo_throw(value_error,"invalid value for the first vertex");
	}


	size_t first_city, Nt;
	if(m_start_city == -1){
		first_city = 0;  
	  		Nt = Nv;
	}
	else{
		first_city = m_start_city; 
		Nt = m_start_city+1;
	}

	int length_best_tour, length_new_tour;
	size_t nxt_city, min_idx;
	std::vector<int> not_visited(Nv);
	length_best_tour = 0;

	//main loop
	for (size_t i = first_city; i < Nt; i++) {
		length_new_tour = 0;
		for (size_t j = 0; j < Nv; j++) {
			not_visited[j] = j;
		}
		new_tour[0] = i;
		std::swap(not_visited[new_tour[0]],not_visited[Nv-1]);
		for (size_t j = 1; j < Nv-1; j++) {
			min_idx = 0;
			nxt_city = not_visited[0];
			for (size_t l = 1; l < Nv-j; l++) {
				if(prob->distance(new_tour[j-1], not_visited[l]) < prob->distance(new_tour[j-1], nxt_city) )
			{
					min_idx = l;		
					nxt_city = not_visited[l];}
			}
			new_tour[j] = nxt_city;
			length_new_tour += prob->distance(new_tour[j-1], nxt_city);
			std::swap(not_visited[min_idx],not_visited[Nv-j-1]);
		}
		new_tour[Nv-1] = not_visited[0];
		length_new_tour += prob->distance(new_tour[Nv-2], new_tour[Nv-1]);
		length_new_tour += prob->distance(new_tour[Nv-1], new_tour[0]);
		if(i == first_city || length_new_tour < length_best_tour){
			best_tour = new_tour;
			length_best_tour = length_new_tour;
		}
	}
		
	//change representation of tour
	population::size_type best_idx = pop.get_best_idx();
	switch( prob->get_encoding() ) {
	    case problem::base_tsp::FULL:
	        pop.set_x(best_idx,prob->cities2full(best_tour));
	        break;
	    case problem::base_tsp::RANDOMKEYS:
	        pop.set_x(best_idx,prob->cities2randomkeys(best_tour,pop.get_individual(best_idx).cur_x));
	        break;
	    case problem::base_tsp::CITIES:
	        pop.set_x(best_idx,best_tour);
	        break;
	}

} // end of evolve
    

	
    /// Algorithm name
    std::string nn_tsp::get_name() const
    {
        return "Nearest neighbour algorithm";
    }

}} //namespaces

BOOST_CLASS_EXPORT_IMPLEMENT(pagmo::algorithm::nn_tsp)
