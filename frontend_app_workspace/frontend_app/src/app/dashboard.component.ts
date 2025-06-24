import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  template: `
    <section class="dashboard-placeholder">
      <h2>Dashboard</h2>
      <p>This is your expense overview. Charts and analytics coming soon.</p>
    </section>
  `,
})
export class DashboardComponent {}
