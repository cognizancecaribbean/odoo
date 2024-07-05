/** @odoo-module **/

import { Component, props } from "@odoo/owl";

class TotalsCard extends Component {
    static props = {
        title: String,
        total: Number,
    };
}

TotalsCard.template = "artisan_management.TotalsCard";

export default TotalsCard;
