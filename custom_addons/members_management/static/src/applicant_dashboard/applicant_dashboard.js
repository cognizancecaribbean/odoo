/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";
import TotalsCard from "./totals_card"; 


class ApplicantDashboard extends Component {
    setup() {
        this.state = useState({
            totalApplicants: 0,
            totalNewApplicants: 0,
            totalAcknowledgedApplicants: 0,
            totalInterviewApplicants: 0,
            totalFollowupApplicants: 0,
            totalWelcomedApplicants: 0,
            totalOrientationApplicants: 0,
            totalApplicantsSentBylaws: 0,
            totalApplicantsSentQuotes: 0,
            totalApplicantsSignedQuotes: 0,
            totalApplicantsSubInitialized: 0,
        });

        onMounted(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            const totals = await jsonrpc("/applicants_dashboard/get_totals", {});
            this.state.totalApplicants = totals.total_applicants;
            this.state.totalNewApplicants = totals.total_new_applicants;
            this.state.totalAcknowledgedApplicants = totals.total_acknowledged_applicants;
            this.state.totalInterviewApplicants = totals.total_interview_applicants;
            this.state.totalFollowupApplicants = totals.total_followup_applicants;
            this.state.totalWelcomedApplicants = totals.total_welcomed_applicants;
            this.state.totalOrientationApplicants = totals.total_orientation_applicants;
            this.state.totalApplicantsSentBylaws = totals.total_applicants_sent_bylaws;
            this.state.totalApplicantsSentQuotes = totals.total_applicants_sent_quotes;
            this.state.totalApplicantsSignedQuotes = totals.total_applicants_signed_quotes;
            this.state.totalApplicantsSignedQuotes = totals.total_applicants_sub_initialized;
        } catch (error) {
            console.error("Error loading dashboard data:", error);
        }
    }

    getActionUrl(actionName) {
        return `/web#action=${actionName}`;
    }

}

ApplicantDashboard.components = { TotalsCard };  // Register the components

ApplicantDashboard.template = "members_management.ApplicantDashboardUI";

registry.category("actions").add("applicant_dashboard", ApplicantDashboard);
