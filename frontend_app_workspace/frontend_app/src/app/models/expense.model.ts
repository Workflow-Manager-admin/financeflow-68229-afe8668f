export interface Expense {
  id: number;
  amount: number;
  description: string;
  date: string; // ISO string
  category: Category | number; // could be category object or id
  created_at?: string; // ISO string, optional
  updated_at?: string; // ISO string, optional
}

export interface Category {
  id: number;
  name: string;
  color?: string; // for frontend use in charts, etc.
  description?: string;
}

export interface DashboardSummary {
  totalExpense: number;
  monthlyExpense: number;
  categories: CategorySummary[];
  recentExpenses: Expense[];
}

export interface CategorySummary {
  category: Category;
  total: number;
  percent: number;
}
