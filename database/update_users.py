from sqlalchemy import text
from connectDB import engine

def update_user(user_id, username, password, role):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE Users
                SET
                    Username = :username,
                    Password = :password,
                    Role = :role
                WHERE Id = :id
            """),
            {
                "id": user_id,
                "username": username,
                "password": password,
                "role": role
            }
        )

    print("Users updated successfully!")


# Exemple
update_user(
    user_id=1,
    username="rodrigue",
    password="new_password",
    role="Admin"
)


###################################################
### Mise à jour du mot de passe uniquement 
#######

#def update_password(user_id, new_password):

    #with engine.begin() as conn:

        #conn.execute(
            #text("""
                #UPDATE Users
                #SET Password = :password
                #WHERE Id = :id
            #"""),
            #{
                #"id": user_id,
                #"password": new_password
           # }
        #)
