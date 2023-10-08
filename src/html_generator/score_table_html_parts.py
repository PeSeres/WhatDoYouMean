score_table_head_part = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>"What do you mean?" Eremények</title>
            <style>            
                h1 {
                  font-size: 40px;
                  text-align: center;
                  margin: 20px;
                  text-shadow: 2px 2px #dddddd;
                }

                #tables {
                    display: flex;
                    justify-content: space-between;
                    border: 3px solid #fff;
                    padding: 20px;
                }

                .table-container {
                    margin: 1%;
                    width: 50%;
                    float: left;
                    padding: 20px;
                    border: 2px solid #BEBEBE;
                }

                table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 80%;
                    font-size: 30px;
                    margin: 0 auto;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }

                td, th {
                    text-align: center;
                    border: 1px solid #dddddd;
                    padding: 8px;
                    font-size: 35px;
                }

                tr:nth-child(even) {
                    background-color: #dddddd;
                }

                 .table-title{
                    font-size: 45px;
                 }
            </style>
        </head>
        <body>
            <h1>Eredmények</h1>
    """

score_table_tail_part = f"""
        </body>
    </html>
    """
