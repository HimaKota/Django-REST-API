<h1><b>Final Project Links (Arranged According To Usage)</b></h1>

<h3>1. Admin Access</h3>
    Admin Section: http://127.0.0.1:8000/dashboard/


<h3>2. Accounts</h3>

    Registration: http://127.0.0.1:8000/api/account/register/
    Login: http://127.0.0.1:8000/api/account/login/
    Logout: http://127.0.0.1:8000/api/account/logout/

<h3>3. Stream Platforms</h3>

    Create Element & Access List: http://127.0.0.1:8000/api/watch/stream/
    Access, Update & Destroy Individual Element: http://127.0.0.1:8000/api/watch/stream/<int:streamplatform_id>/

<h3>4. Watch List</h3>

    Create & Access List: http://127.0.0.1:8000/api/watch/
    Access, Update & Destroy Individual Element: http://127.0.0.1:8000/api/watch/<int:movie_id>/

<h3>5. Reviews</h3>

    Create Review For Specific Movie: http://127.0.0.1:8000/api/watch/<int:movie_id>/reviews/create/
    List Of All Reviews For Specific Movie: http://127.0.0.1:8000/api/watch/<int:movie_id>/reviews/
    Access, Update & Destroy Individual Review: http://127.0.0.1:8000/api/watch/reviews/<int:review_id>/

<h3>6. User Review</h3>

    Access All Reviews For Specific User: http://127.0.0.1:8000/api/watch/user-reviews/?username=example
