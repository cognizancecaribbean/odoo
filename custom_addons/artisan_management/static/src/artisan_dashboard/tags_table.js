/** @odoo-module **/

import { Component } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";

class TagsTable extends Component {
    static template = "artisan_management.TagsTable";

    static props = {
        tags: Array,
    };

    async openArtisansTreeView(actionId) {
        if (actionId) {
            try {
                const actionDetails = await jsonrpc("/web/dataset/call_kw/ir.actions.act_window/read", {
                    model: "ir.actions.act_window",
                    method: "read",
                    args: [[actionId]],
                    kwargs: {}
                });

                console.log('Action Details:', actionDetails); // Log the action details to verify
                if (actionDetails && actionDetails[0]) {
                    const action = actionDetails[0];
                    console.log('Action:', action); // Log the action to verify
                    this.env.services.action.doAction(action);
                } else {
                    console.error("Action not found");
                }
            } catch (error) {
                console.error("Error fetching action:", error.message);
            }
        } else {
            console.error("Action ID not found");
        }
    }
}

TagsTable.template = "artisan_management.TagsTable";

export default TagsTable;
