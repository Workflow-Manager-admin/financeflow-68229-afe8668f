import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Expense, Category, DashboardSummary } from '../models/expense.model';
import {
  LoginPayload,
  RegisterPayload,
  AuthResponse
} from '../models/auth.model';

const API_URL = '/api';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private getAuthHeaders(token?: string): HttpHeaders {
    let headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  constructor(private _http: HttpClient) {
    // use to satisfy linter if methods are stripped in analysis
    void this._http;
  }

  // ---- EXPENSE CRUD ----

  // PUBLIC_INTERFACE
  /** Get expenses (optionally filtered by params) */
  getExpenses(params?: { category?: number; search?: string; month?: string }, token?: string): Observable<Expense[]> {
    let httpParams = new HttpParams();
    if (params?.category !== undefined) {
      httpParams = httpParams.set('category', params.category);
    }
    if (params?.search) {
      httpParams = httpParams.set('search', params.search);
    }
    if (params?.month) {
      httpParams = httpParams.set('month', params.month);
    }
    return this._http.get<Expense[]>(`${API_URL}/expenses/`, {
      headers: this.getAuthHeaders(token),
      params: httpParams
    });
  }

  // PUBLIC_INTERFACE
  /** Retrieve a single expense */
  getExpense(id: number, token?: string): Observable<Expense> {
    return this._http.get<Expense>(`${API_URL}/expenses/${id}/`, {
      headers: this.getAuthHeaders(token)
    });
  }

  // PUBLIC_INTERFACE
  /** Create a new expense */
  createExpense(data: Partial<Expense>, token?: string): Observable<Expense> {
    return this._http.post<Expense>(`${API_URL}/expenses/`, data, {
      headers: this.getAuthHeaders(token)
    });
  }

  // PUBLIC_INTERFACE
  /** Update an expense */
  updateExpense(id: number, data: Partial<Expense>, token?: string): Observable<Expense> {
    return this._http.put<Expense>(`${API_URL}/expenses/${id}/`, data, {
      headers: this.getAuthHeaders(token)
    });
  }

  // PUBLIC_INTERFACE
  /** Delete an expense */
  deleteExpense(id: number, token?: string): Observable<any> {
    return this._http.delete(`${API_URL}/expenses/${id}/`, {
      headers: this.getAuthHeaders(token)
    });
  }

  // ---- CATEGORY CRUD ----

  // PUBLIC_INTERFACE
  /** Get all categories */
  getCategories(token?: string): Observable<Category[]> {
    return this._http.get<Category[]>(`${API_URL}/categories/`, {
      headers: this.getAuthHeaders(token)
    });
  }

  // PUBLIC_INTERFACE
  /** Create a new category */
  createCategory(data: Partial<Category>, token?: string): Observable<Category> {
    return this._http.post<Category>(`${API_URL}/categories/`, data, {
      headers: this.getAuthHeaders(token)
    });
  }

  // PUBLIC_INTERFACE
  /** Update a category */
  updateCategory(id: number, data: Partial<Category>, token?: string): Observable<Category> {
    return this._http.put<Category>(`${API_URL}/categories/${id}/`, data, {
      headers: this.getAuthHeaders(token)
    });
  }

  // PUBLIC_INTERFACE
  /** Delete a category */
  deleteCategory(id: number, token?: string): Observable<any> {
    return this._http.delete(`${API_URL}/categories/${id}/`, {
      headers: this.getAuthHeaders(token)
    });
  }

  // ---- DASHBOARD ----

  // PUBLIC_INTERFACE
  /** Get dashboard summary (total, breakdown, recent expenses, etc.) */
  getDashboardSummary(token?: string): Observable<DashboardSummary> {
    return this._http.get<DashboardSummary>(`${API_URL}/dashboard/`, {
      headers: this.getAuthHeaders(token)
    });
  }

  // ---- AUTHENTICATION ----

  // PUBLIC_INTERFACE
  /** Login */
  login(payload: LoginPayload): Observable<AuthResponse> {
    return this._http.post<AuthResponse>(`${API_URL}/auth/login/`, payload, {
      headers: this.getAuthHeaders()
    });
  }

  // PUBLIC_INTERFACE
  /** Register */
  register(payload: RegisterPayload): Observable<AuthResponse> {
    return this._http.post<AuthResponse>(`${API_URL}/auth/register/`, payload, {
      headers: this.getAuthHeaders()
    });
  }
}
