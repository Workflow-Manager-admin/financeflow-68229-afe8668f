import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard.component';
import { ExpensesComponent } from './expenses.component';
import { CategoriesComponent } from './categories.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent, title: 'Dashboard' },
  { path: 'expenses', component: ExpensesComponent, title: 'Expenses' },
  { path: 'categories', component: CategoriesComponent, title: 'Categories' },
  { path: '**', redirectTo: 'dashboard' }
];
