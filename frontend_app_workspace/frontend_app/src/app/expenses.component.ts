import { Component } from '@angular/core';

@Component({
  selector: 'app-expenses',
  standalone: true,
  template: `
    <section class="expenses-placeholder">
      <h2>Expenses</h2>
      <p>List and manage your expenses here. CRUD UX coming soon.</p>
    </section>
  `
})
export class ExpensesComponent {}
