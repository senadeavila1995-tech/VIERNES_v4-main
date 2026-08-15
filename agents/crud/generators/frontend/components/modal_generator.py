from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class ModalGenerator(BaseFrontendGenerator):

    name = "frontend_modal"

    description = "Genera modal React."

    order = 85

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = self.modal_name(context)

        return f"""

import React from "react";


interface Props {{

children: React.ReactNode;

open:boolean;

onClose:()=>void;

}}



export default function {component}({{

children,

open,

onClose


}}:Props){{



if(!open)

return null;



return (

<div className="modal show d-block">


<div className="modal-dialog">


<div className="modal-content">


<div className="modal-header">


<h5>

{context.entity_name}

</h5>


<button

className="btn-close"

onClick={{onClose}}

>

</button>


</div>



<div className="modal-body">

{{children}}

</div>


</div>


</div>


</div>

)

}}

"""
