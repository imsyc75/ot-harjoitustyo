# Arkkitehtuurikuvaus
HUOM! Lisään Repository Pattern-tyyppisen rakenteen myöhemmin, tämä johtaa valtaviin rakenteellisiin muutoksiin. Joten en kirjoita paljon sisältöä arkkitehtuurille juuri nyt. 

## Rakenne
koodin pakkausrakenne on seuraava:
![Pakkausrakenne](./pics/arkkitehtuuri_pakkaus.png)
Pakkaus _ui_ sisältää kaikki käyttöliittymänäkymät, käsittelee käyttäjän vuorovaikutusta ja tietojen näyttöä. _Entitles_ sisältää sovelluksen tietomallin.

## Käyttöliittymä

Sovelluksen käyttöliittymä koostuu neljästä eri näkymästä:

- Kirjaudu sisään
- Luo uusi käyttäjä
- Päänäkymä, jossa luetellaan käyttäjän kulut.
- Luo työnkulku (muokkaa samalla sivulla)

Kaikki näkymät toteutetaan omassa luokassaan. Menojen muokkaus- ja poistoikkunat on toteutettu metodeina päänäkymässä.

## Sovelluslogiikka

Sovelluksen loogisen tietomallin muodostavat luokat [User](/src/entities/user.py) ja [Expense](/src/entities/expenses.py), jotka kuvaavat käyttäjiä ja käyttäjien kuluja:

```mermaid
 classDiagram
      Expense "*" --> "1" User
      class User{
          username
          password
      }
      class Expense{
        id,
        user_id,
        amount,
        category,
        date,
        description
      }
```
## Sovelluksen päätoiminnallisuudet

### Käyttäjän luominen

```mermaid
sequenceDiagram
    actor User
    participant RegisterView
    participant User_Class
    participant Database
    
    User->>RegisterView: Enter username and password
    User->>RegisterView: Click "Submit" button
    RegisterView->>RegisterView: handle_register()
    RegisterView->>User_Class: create User(username, password)
    RegisterView->>User_Class: user_obj.create()
    User_Class->>Database: get_db_connection()
    User_Class->>Database: INSERT INTO users
    Database-->>User_Class: Result (success/failure)
    User_Class-->>RegisterView: True/False
    RegisterView-->>User: Show success/error message
```

### Käyttäjän kirjautuminen

```mermaid
sequenceDiagram
    actor User
    participant LoginView
    participant User_Class
    participant Database
    participant ExpensesView
    
    User->>LoginView: Enter username and password
    User->>LoginView: Click "Login" button
    LoginView->>LoginView: handle_login()
    LoginView->>User_Class: create User(username)
    LoginView->>User_Class: user_obj.find_by_username()
    User_Class->>Database: get_db_connection()
    User_Class->>Database: SELECT FROM users
    Database-->>User_Class: user_data
    User_Class-->>LoginView: user_data
    LoginView->>LoginView: Check password
  ```

### Uuden kulun luominen

Uuden kulun luovan "Add Expense" painikkeen klikkaamisen seurauksena tapahtuva sovelluksen toimintalogiikka sekvenssikaaviona:

```mermaid
sequenceDiagram
    actor User
    participant ExpensesView
    participant AddExpenseView
    participant Expense_Class
    participant Database
    
    User->>ExpensesView: Click "Add New Expense"
    ExpensesView->>ExpensesView: open_add_expense()
    ExpensesView->>AddExpenseView: Create AddExpenseView
    AddExpenseView-->>User: Show add expense form
    User->>AddExpenseView: Enter expense details
    User->>AddExpenseView: Click "Save" button
    AddExpenseView->>AddExpenseView: save_expense()
    AddExpenseView->>AddExpenseView: Validate inputs
    AddExpenseView->>Expense_Class: Create Expense with user_id and details
    AddExpenseView->>Expense_Class: expense.create()
    Expense_Class->>Database: get_db_connection()
    Expense_Class->>Database: INSERT INTO expenses
    Database-->>Expense_Class: Result (success/failure)
    Expense_Class-->>AddExpenseView: True/False
    AddExpenseView-->>User: Show success/error message
    AddExpenseView->>AddExpenseView: destroy()
    ExpensesView->>ExpensesView: load_expenses()
    ExpensesView->>Expense_Class: Create Expense with user_id
    ExpensesView->>Expense_Class: expense_obj.get_expenses_by_date_range()
    Expense_Class->>Database: SELECT FROM expenses
    Database-->>Expense_Class: expenses
    Expense_Class-->>ExpensesView: expenses
    ExpensesView-->>User: Show updated expenses list
```

### Kulun muokkaminen
```mermaid
sequenceDiagram
    actor User
    participant ExpensesView
    participant AddExpenseView
    participant Expense_Class
    participant Database
    
    User->>ExpensesView: Select an expense
    User->>ExpensesView: Click "Edit Selected"
    ExpensesView->>ExpensesView: edit_selected_expense()
    ExpensesView->>ExpensesView: get_selected_expense_id()
    ExpensesView->>Expense_Class: Create Expense with user_id
    ExpensesView->>Expense_Class: expense_obj.get_by_id(expense_id)
    Expense_Class->>Database: get_db_connection()
    Expense_Class->>Database: SELECT FROM expenses
    Database-->>Expense_Class: expense_data
    Expense_Class-->>ExpensesView: expense_data
    ExpensesView->>AddExpenseView: Create AddExpenseView with expense_data
    AddExpenseView-->>User: Show edit form with expense data
    User->>AddExpenseView: Modify expense details
    User->>AddExpenseView: Click "Save" button
    AddExpenseView->>AddExpenseView: save_expense()
    AddExpenseView->>Expense_Class: Create Expense with user_id and details
    AddExpenseView->>Expense_Class: expense.update(expense_id)
    Expense_Class->>Database: get_db_connection()
    Expense_Class->>Database: UPDATE expenses
    Database-->>Expense_Class: Result (success/failure)
    Expense_Class-->>AddExpenseView: True/False
    AddExpenseView-->>User: Show success/error message
    AddExpenseView->>AddExpenseView: destroy()
    ExpensesView->>ExpensesView: load_expenses()
    ExpensesView->>Expense_Class: Get expenses for current month/year
    Expense_Class->>Database: SELECT FROM expenses
    Database-->>Expense_Class: expenses
    Expense_Class-->>ExpensesView: expenses
    ExpensesView-->>User: Show updated expenses list
```

### Kulun poistaminen
```mermaid
sequenceDiagram
    actor User
    participant ExpensesView
    participant Expense_Class
    participant Database
    
    User->>ExpensesView: Select an expense
    User->>ExpensesView: Click "Delete Selected"
    ExpensesView->>ExpensesView: delete_selected_expense()
    ExpensesView->>ExpensesView: get_selected_expense_id()
    ExpensesView-->>User: Show confirmation dialog
    User->>ExpensesView: Confirm deletion
    ExpensesView->>Expense_Class: Create Expense with user_id
    ExpensesView->>Expense_Class: expense_obj.delete(expense_id)
    Expense_Class->>Database: get_db_connection()
    Expense_Class->>Database: DELETE FROM expenses
    Database-->>Expense_Class: Result (success/failure)
    Expense_Class-->>ExpensesView: True/False
    ExpensesView-->>User: Show success/error message
    ExpensesView->>ExpensesView: load_expenses()
    ExpensesView->>Expense_Class: Get expenses for current month/year
    Expense_Class->>Database: SELECT FROM expenses
    Database-->>Expense_Class: expenses
    Expense_Class-->>ExpensesView: expenses
    ExpensesView-->>User: Show updated expenses list
```
