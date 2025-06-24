import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ChartConfiguration, ChartType, ChartOptions } from 'chart.js';
import { CommonModule } from '@angular/common';
import { NgChartsModule } from 'ng2-charts';
import { DashboardSummary, Category } from './models/expense.model';

// PUBLIC_INTERFACE
@Component({
  selector: 'app-dashboard-charts',
  standalone: true,
  imports: [CommonModule, NgChartsModule],
  template: `
    <section *ngIf="summary">
      <div style="display: flex; gap:2rem; flex-wrap:wrap;">
        <div class="chart-card">
          <h3>Total Expenses by Category</h3>
          <canvas baseChart
            [data]="pieChartData"
            [type]="pieChartType"
            [options]="pieChartOptions">
          </canvas>
        </div>
        <div class="chart-card">
          <h3>Monthly Trend</h3>
          <canvas baseChart
            [data]="lineChartData"
            [type]="lineChartType"
            [options]="lineChartOptions">
          </canvas>
        </div>
        <div class="summary-card">
          <h3>Summary</h3>
          <ul>
            <li><b>Total Expenses:</b> {{ summary?.totalExpense | currency:'USD':'symbol':'1.2-2' }}</li>
            <li><b>This Month:</b> {{ summary?.monthlyExpense | currency:'USD':'symbol':'1.2-2' }}</li>
            <li><b>Categories:</b> {{ summary?.categories?.length || 0 }}</li>
          </ul>
        </div>
      </div>
      <div style="margin-top:2.5rem;">
        <h3>Recent Expenses</h3>
        <table *ngIf="summary?.recentExpenses?.length; else noRecent" class="recent-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Category</th>
              <th>Description</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let exp of summary?.recentExpenses">
              <td>{{ exp.date | date: 'yyyy-MM-dd'}}</td>
              <td>{{ categoryName(exp.category) }}</td>
              <td>{{ exp.description }}</td>
              <td>{{ exp.amount | currency:'USD':'symbol':'1.2-2' }}</td>
            </tr>
          </tbody>
        </table>
        <ng-template #noRecent>
          <div style="color:#aaa;text-align:center;">No recent expenses.</div>
        </ng-template>
      </div>
    </section>
  `,
  styleUrls: []
})
export class DashboardChartsComponent implements OnChanges {
  @Input() summary?: DashboardSummary;

  pieChartType: ChartType = 'pie';
  pieChartData: ChartConfiguration['data'] = { labels: [], datasets: [{ data: [] }] };
  pieChartOptions: ChartOptions = { responsive: true, plugins: { legend: { position: 'right' } } };

  lineChartType: ChartType = 'line';
  lineChartData: ChartConfiguration['data'] = { labels: [], datasets: [{ data: [], label: 'Expense' }] };
  lineChartOptions: ChartOptions = {
    responsive: true,
    plugins: { legend: { display: false } }
  };

  ngOnChanges(changes: SimpleChanges) {
    if (changes['summary']) {
      this.preparePieChart();
      this.prepareLineChart();
    }
  }

  private preparePieChart() {
    if (!this.summary) return;
    this.pieChartData = {
      labels: this.summary.categories.map(cs => cs.category.name),
      datasets: [{
        data: this.summary.categories.map(cs => +cs.total),
        backgroundColor: this.summary.categories.map(cs => cs.category.color || this.randomColor()),
      }]
    };
  }

  private prepareLineChart() {
    // Assuming recentExpenses have dates; aggregate by month for simple trend.
    if (!this.summary?.recentExpenses) return;
    const byMonth = new Map<string, number>();
    for (const exp of this.summary.recentExpenses) {
      const ym = exp.date.slice(0, 7); // 'YYYY-MM'
      byMonth.set(ym, (byMonth.get(ym) || 0) + +exp.amount);
    }
    const months = [...byMonth.keys()].sort();
    this.lineChartData = {
      labels: months,
      datasets: [{
        data: months.map(m => byMonth.get(m) ?? 0),
        label: 'Monthly Expenses',
        fill: false,
        tension: 0.2,
        borderColor: '#1976d2',
        backgroundColor: '#42a5f5'
      }]
    };
  }

  categoryName(cat: Category | number): string {
    if (!this.summary?.categories) return '';
    if (typeof cat === 'object') return cat.name;
    const c = this.summary.categories.find(cs => cs.category.id === cat);
    return c ? c.category.name : String(cat);
  }

  private randomColor(): string {
    // For any category without defined color
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
}
