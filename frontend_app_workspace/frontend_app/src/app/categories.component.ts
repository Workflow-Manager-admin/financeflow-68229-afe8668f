import { Component } from '@angular/core';
import { Category } from './models/expense.model';
import { CategoryListComponent } from './category-list.component';
import { ApiService } from './services/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule, CategoryListComponent],
  template: `
    <section>
      <h2>Categories</h2>
      <app-category-list
        [categories]="categories"
        [loading]="loading"
        (addCategory)="addCategory($event)"
        (editCategory)="editCategory($event)"
        (deleteCategory)="deleteCategory($event)"
      ></app-category-list>
    </section>
  `,
  styleUrls: []
})
export class CategoriesComponent {
  categories: Category[] = [];
  loading = false;
  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadCategories();
  }

  loadCategories() {
    this.loading = true;
    this.api.getCategories().subscribe(cats => {
      this.categories = cats;
      this.loading = false;
    }, () => this.loading = false);
  }
  addCategory(data: Partial<Category>) {
    this.api.createCategory(data).subscribe(() => this.loadCategories());
  }
  editCategory(cat: Category) {
    const { id, ...data } = cat;
    this.api.updateCategory(id, data).subscribe(() => this.loadCategories());
  }
  deleteCategory(cat: Category) {
    this.api.deleteCategory(cat.id).subscribe(() => this.loadCategories());
  }
}
