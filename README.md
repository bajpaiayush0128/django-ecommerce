# Django Ecommerce

This repository contains a Django-based web application of an ecommerce site. The application allows users to buy products online and pay using their cards.

## Features

- User registration and authentication(using email verification)
- option to reset password
- users can add items to their cart and place order from there
- payment integration using stripe
- users can view their profile and orders

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bajpaiayush0128/django-ecommerce.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django-ecommerce
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Apply the database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://localhost:8000` in your web browser.

9. Add gmail and password in settings.py for email authentication to work and stripe keys in keys.py for payment integration (look stripe docs for help at stripe.com/docs)

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

Please ensure that your code adheres to the existing coding style and conventions used in the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgements

- The Django framework
- [Bootstrap](https://getbootstrap.com) for the front-end design
- Other open-source libraries and dependencies used in this project
