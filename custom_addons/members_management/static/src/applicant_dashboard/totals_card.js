/** @odoo-module **/

import { Component, props } from "@odoo/owl";

class TotalsCard extends Component {
    static props = {
        title: String,
        total: Number,
        actionUrl: String,
    };
}

TotalsCard.template = "members_management.TotalsCard";

export default TotalsCard;
