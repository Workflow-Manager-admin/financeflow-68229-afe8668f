import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './services/api.service';
import { DashboardChartsComponent } from './dashboard-charts.component';
import { DashboardSummary } from './models/expense.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, DashboardChartsComponent],
  template: `
    <section>
      <h2>Dashboard</h2>
      <app-dashboard-charts [summary]="summary"></app-dashboard-charts>
      <div *ngIf="loading" style="text-align:center;color:#888;">Loading...</div>
      <div *ngIf="error" style="color:red;text-align:center;">Failed to load dashboard data.</div>
    </section>
  `,
})
export class DashboardComponent {
  summary?: DashboardSummary;
  loading = false;
  error = false;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loading = true;
    this.error = false;
    this.api.getDashboardSummary().subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.error = true;
      }
    });
  }
}
