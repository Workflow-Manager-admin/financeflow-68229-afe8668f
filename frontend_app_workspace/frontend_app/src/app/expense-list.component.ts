import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Expense, Category } from './models/expense.model';
import { FormsModule } from '@angular/forms';

// PUBLIC_INTERFACE
@Component({
  selector: 'app-expense-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './expense-list.component.html',
  styleUrls: []
})
export class ExpenseListComponent {
  @Input() expenses: Expense[] = [];
  @Input() categories: Category[] = [];
  @Input() loading: boolean = false;
  @Input() showCategoryFilter = true;
  @Input() token?: string;

  @Output() editExpense = new EventEmitter<Expense>();
  @Output() deleteExpense = new EventEmitter<Expense>();

  filterCategory: number | '' = '';
  filterSearch = '';

  get filteredExpenses(): Expense[] {
    let filtered = [...this.expenses];
    if (this.filterCategory) {
      filtered = filtered.filter(e => (typeof e.category === 'object' ? e.category.id : e.category) === +this.filterCategory);
    }
    if (this.filterSearch) {
      const search = this.filterSearch.toLowerCase();
      filtered = filtered.filter(
        e =>
          e.description.toLowerCase().includes(search) ||
          (typeof e.category === 'object' ? e.category.name.toLowerCase().includes(search) : false)
      );
    }
    return filtered;
  }

  onEdit(expense: Expense) {
    this.editExpense.emit(expense);
  }
  onDelete(expense: Expense) {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      this.deleteExpense.emit(expense);
    }
  }

  categoryName(category: Category | number): string {
    if (typeof category === 'object') return category.name;
    const found = this.categories.find(c => c.id === category);
    return found ? found.name : '';
  }
}
