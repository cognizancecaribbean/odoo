/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class BoatyardMap extends Component {
    // Function to handle clicking on boat spots
    onSpotClick(ev) {
        const spotName = ev.target.dataset.spot;  // Get spot name from data attribute
        alert(`You clicked on ${spotName}!`);
    }
}

// Registering the Boatyard Map action
BoatyardMap.template = "boatyard_management.BoatyardMapUI";

registry.category("actions").add("boatyard_map", BoatyardMap);

