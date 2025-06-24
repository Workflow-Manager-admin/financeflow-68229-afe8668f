import { Component } from '@angular/core';
import { ExpenseListComponent } from './expense-list.component';
import { ExpenseFormComponent } from './expense-form.component';
import { ApiService } from './services/api.service';
import { Expense, Category } from './models/expense.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-expenses',
  standalone: true,
  imports: [CommonModule, ExpenseListComponent, ExpenseFormComponent],
  template: `
    <section>
      <h2>Expenses</h2>
      <button (click)="startAdd()" style="margin-bottom:1em;">Add Expense</button>
      <app-expense-form
        *ngIf="formMode"
        [expense]="editingExpense"
        [categories]="categories"
        (save)="onSave($event)"
        (cancel)="cancelForm()"
      ></app-expense-form>
      <app-expense-list
        [expenses]="expenses"
        [categories]="categories"
        [loading]="loading"
        (editExpense)="startEdit($event)"
        (deleteExpense)="deleteExpense($event)"
      ></app-expense-list>
    </section>
  `,
  styleUrls: []
})
export class ExpensesComponent {
  expenses: Expense[] = [];
  categories: Category[] = [];
  loading = false;
  formMode = false;
  editingExpense?: Expense | null = null;
  constructor(public api: ApiService) {}

  ngOnInit() {
    this.loadEverything();
  }

  loadEverything() {
    this.loading = true;
    this.api.getCategories().subscribe((cats: Category[]) => { this.categories = cats; });
    this.api.getExpenses().subscribe((items: Expense[]) => {
      this.expenses = items;
      this.loading = false;
    }, () => this.loading = false);
  }
  startAdd() {
    this.formMode = true;
    this.editingExpense = null;
  }
  startEdit(exp: Expense) {
    this.formMode = true;
    this.editingExpense = exp;
  }
  cancelForm() {
    this.formMode = false;
    this.editingExpense = null;
  }
  onSave(data: Partial<Expense>) {
    if (this.editingExpense) {
      this.api.updateExpense(this.editingExpense.id, data).subscribe(() => {
        this.loadEverything();
        this.cancelForm();
      });
    } else {
      this.api.createExpense(data).subscribe(() => {
        this.loadEverything();
        this.cancelForm();
      });
    }
  }
  deleteExpense(exp: Expense) {
    this.api.deleteExpense(exp.id).subscribe(() => this.loadEverything());
  }
}
