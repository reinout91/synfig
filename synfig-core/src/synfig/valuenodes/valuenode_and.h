/* === S Y N F I G ========================================================= */
/*!	\file valuenode_and.h
**	\brief Header file for implementation of the "And" valuenode conversion.
**
**	\legal
**	Copyright (c) 2002-2005 Robert B. Quattlebaum Jr., Adrian Bentley
**	Copyright (c) 2009 Nikita Kitaev
**  Copyright (c) 2011 Carlos López
**
**	This file is part of Synfig.
**
**	Synfig is free software: you can redistribute it and/or modify
**	it under the terms of the GNU General Public License as published by
**	the Free Software Foundation, either version 2 of the License, or
**	(at your option) any later version.
**
**	Synfig is distributed in the hope that it will be useful,
**	but WITHOUT ANY WARRANTY; without even the implied warranty of
**	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**	GNU General Public License for more details.
**
**	You should have received a copy of the GNU General Public License
**	along with Synfig.  If not, see <https://www.gnu.org/licenses/>.
**	\endlegal
*/
/* ========================================================================= */

/* === S T A R T =========================================================== */

#ifndef __SYNFIG_VALUENODE_AND_H
#define __SYNFIG_VALUENODE_AND_H

/* === H E A D E R S ======================================================= */

#include <synfig/valuenode.h>

/* === M A C R O S ========================================================= */

/* === C L A S S E S & S T R U C T S ======================================= */

namespace synfig {

class ValueNode_And : public LinkableValueNode
{
	ValueNode::RHandle link1_;
	ValueNode::RHandle link2_;

	ValueNode_And(const ValueBase &x);

public:
	typedef etl::handle<ValueNode_And> Handle;
	typedef etl::handle<const ValueNode_And> ConstHandle;

	static ValueNode_And* create(const ValueBase& x, etl::loose_handle<Canvas> canvas=nullptr);
	virtual ~ValueNode_And();

	virtual ValueBase operator()(Time t) const override;

	virtual String get_name() const override;
	virtual String get_local_name() const override;
	static bool check_type(Type &type);

protected:
	LinkableValueNode* create_new() const override;

	virtual bool set_link_vfunc(int i,ValueNode::Handle x) override;
	virtual ValueNode::LooseHandle get_link_vfunc(int i) const override;

	virtual LinkableValueNode::Vocab get_children_vocab_vfunc() const override;
}; // END of class ValueNode_And

}; // END of namespace synfig

/* === E N D =============================================================== */

#endif
