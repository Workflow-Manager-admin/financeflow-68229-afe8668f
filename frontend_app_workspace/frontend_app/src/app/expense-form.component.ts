import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Category, Expense } from './models/expense.model';
import { FormsModule } from '@angular/forms';

// PUBLIC_INTERFACE
@Component({
  selector: 'app-expense-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './expense-form.component.html',
  styleUrls: []
})
export class ExpenseFormComponent {
  @Input() categories: Category[] = [];
  @Input() expense?: Expense | null;
  @Output() save = new EventEmitter<Partial<Expense>>();
  @Output() cancel = new EventEmitter<void>();

  form: Partial<Expense> = {};

  ngOnChanges() {
    if (this.expense) {
      this.form = {
        ...this.expense,
        category: typeof this.expense.category === 'object' ? this.expense.category.id : this.expense.category
      };
    } else {
      this.form = {};
    }
  }

  submitForm() {
    /* eslint-disable no-undef */
    if (!this.form.description || !this.form.amount || !this.form.category || !this.form.date) {
      if (typeof window !== 'undefined' && window.alert) window.alert('Please fill all required fields');
      return;
    }
    /* eslint-enable no-undef */
    this.save.emit(this.form);
  }
}
