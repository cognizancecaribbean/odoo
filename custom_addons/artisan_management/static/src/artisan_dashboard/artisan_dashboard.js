/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";
import TotalsCard from "./totals_card"; 
import TagsTable from "./tags_table"; 

class ArtisanDashboard extends Component {
    setup() {
        this.state = useState({
            totalPending: 0,
            totalVetting: 0,
            totalApproved: 0,
            totalDenied: 0,
            ytdRegistrations: 0,
            ytdApprovals: 0,
            ytdDenials: 0,
            totalsByTag: [],
        });

        onMounted(async () => {
            await this.loadDashboardData();
            // Ensure Chart.js is available before rendering charts
            if (typeof Chart !== 'undefined') {
                this.renderCharts();
            } else {
                console.error("Chart.js is not loaded");
            }
        });
    }

    async loadDashboardData() {
        try {
            const totals = await jsonrpc("/artisan_dashboard/get_totals", {});
            this.state.totalArtisans = totals.total_artisans;
            this.state.totalPending = totals.total_pending;
            this.state.totalVetting = totals.total_vetting;
            this.state.totalApproved = totals.total_approved;
            this.state.totalDenied = totals.total_denied;

            const ytd_totals = await jsonrpc("/artisan_dashboard/get_ytd_totals", {});
            this.state.ytdRegistrations = ytd_totals.ytd_registrations_total;
            this.state.ytdApprovals = ytd_totals.ytd_approvals_total;
            this.state.ytdDenials = ytd_totals.ytd_denials_total;

            this.state.totalsByTag = totals.totals_by_tag;
        } catch (error) {
            console.error("Error loading dashboard data:", error);
        }
    }

    renderCharts() {
        this.renderCurrentStateChart();
        this.renderYTDChart();
        this.renderTagsChart();
    }

    renderCurrentStateChart() {
        const currentStateCtx = document.getElementById('currentStateChart').getContext('2d');
        new Chart(currentStateCtx, {
            type: 'bar',
            data: {
                labels: ['Pending', 'Vetting', 'Approved', 'Denied'],
                datasets: [{
                    label: 'Current State',
                    data: [
                        this.state.totalPending,
                        this.state.totalVetting,
                        this.state.totalApproved,
                        this.state.totalDenied
                    ],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 206, 86, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    renderYTDChart() {
        const ytdCtx = document.getElementById('ytdChart').getContext('2d');
        new Chart(ytdCtx, {
            type: 'bar',
            data: {
                labels: ['Registrations', 'Approvals', 'Denials'],
                datasets: [{
                    label: 'YTD Totals',
                    data: [
                        this.state.ytdRegistrations,
                        this.state.ytdApprovals,
                        this.state.ytdDenials
                    ],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 206, 86, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    renderTagsChart() {
        const tagsCtx = document.getElementById('tagsChart').getContext('2d');
        new Chart(tagsCtx, {
            type: 'bar',
            data: {
                labels: this.state.totalsByTag.map(tag => tag.tag_name),
                datasets: [{
                    label: 'Totals by Tag',
                    data: this.state.totalsByTag.map(tag => tag.count),
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#8A2BE2',
                        '#1E90FF',
                        '#32CD32'
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    getActionUrl(actionName) {
        return `/web#action=${actionName}`;
    }

    getYtdActionUrl(actionName, type) {
        const { startDate, endDate } = this.state;
        return `/web#action=${actionName}&view_type=list&model=artisan.activity.log&domain=[('activity_type','=','${type}'),('activity_date','>=','${startDate}'),('activity_date','<=','${endDate}')]`;
    }
}

ArtisanDashboard.components = { TotalsCard, TagsTable };  // Register the components

ArtisanDashboard.template = "artisan_management.ArtisanDashboardUI";

registry.category("actions").add("artisan_dashboard_action", ArtisanDashboard);
