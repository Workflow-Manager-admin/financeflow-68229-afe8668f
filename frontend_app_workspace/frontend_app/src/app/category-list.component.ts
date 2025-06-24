import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Category } from './models/expense.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// PUBLIC_INTERFACE
@Component({
  selector: 'app-category-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './category-list.component.html',
  styleUrls: []
})
export class CategoryListComponent {
  @Input() categories: Category[] = [];
  @Input() loading: boolean = false;
  @Output() addCategory = new EventEmitter<Partial<Category>>();
  @Output() editCategory = new EventEmitter<Category>();
  @Output() deleteCategory = new EventEmitter<Category>();

  filterSearch = '';
  addMode = false;
  editMode: number | null = null;
  form: Partial<Category> = {};

  get filteredCategories(): Category[] {
    if (!this.filterSearch) return this.categories;
    const search = this.filterSearch.toLowerCase();
    return this.categories.filter(
      c => c.name.toLowerCase().includes(search) || (c.description?.toLowerCase().includes(search) ?? false)
    );
  }

  startAdd() {
    this.addMode = true;
    this.editMode = null;
    this.form = {};
  }
  startEdit(cat: Category) {
    this.addMode = false;
    this.editMode = cat.id;
    this.form = { ...cat };
  }
  submitCategory() {
    if (!this.form.name) {
      window.alert('Name is required!');
      return;
    }
    if (this.editMode) {
      this.editCategory.emit({ ...this.form, id: this.editMode } as Category);
    } else {
      this.addCategory.emit(this.form);
    }
    this.addMode = false;
    this.editMode = null;
    this.form = {};
  }
  cancelEdit() {
    this.addMode = false;
    this.editMode = null;
    this.form = {};
  }
  onDelete(cat: Category) {
    if (window.confirm(`Delete category "${cat.name}"?`)) this.deleteCategory.emit(cat);
  }
}
