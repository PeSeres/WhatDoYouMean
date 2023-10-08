game_page_head_part = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>"What do you mean?" Játék</title>
        <style>     
            #wrapper {
                display: flex;
                border: 3px solid #fff;
                padding: 20px;
                padding-top: 0px;
                width: 100%;
            }
            #right_panel {
                justify-content: space-between;
                border: 3px solid #fff;
                padding: 20px;
                padding-left: 10px;
                padding-top: 0px;
                width: 100%;
            }

            h1 {
              font-size: 30px;
              text-align: center;
              margin: 10px;
              text-shadow: 2px 2px #dddddd;
            }

            p{
                text-align: center;
            }

            #tables {
                display: inline;
                border: 3px solid #fff;
                padding: 20px;
                padding-top: 0px;
                padding-right: 0px;
            }

            .table-container {
                margin: 1%;
                padding: 20px;
                border: 2px solid #BEBEBE;
            }

            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 50%;
                font-size: 15px;
                margin: 0 auto;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            td, th {
                text-align: center;
                border: 1px solid #dddddd;
                padding: 8px;
                font-size: 20px;
            }

            tr:nth-child(even) {
                background-color: #dddddd;
            }

            details {
              cursor: pointer;
              font-size: 30px;
              display: flex;
              align-items: center;
              margin-top: 20px;
            }

            details > * {
                margin: 10px;
            }

            details .questions-container {
                border: 3px solid #fff;
                padding: 20px;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }

            .question-container{
                flex-basis: 40%; 
                margin-right: 10px;
                margin-bottom: 10px;       
                padding: 20px;
                border: 2px solid #BEBEBE;
                font-size: 40px;
            }

            .message-box {
                border: 2px solid #BEBEBE;
                border-radius: 5px;
                padding: 5px;
                margin-top: 10px;
            }

             .table-title{
                font-size: 25px;
             }

             tr.coworker {
                background-color: black;
                color: white;
            }

            #commit-title{
                font-size: 30px;
            }

            #commit-message{
                font-size: 60px;
            }

            #commit-author{
                font-size: 30px;
            }
            #commit-repository{
                font-size: 30px;
            }

        </style>
    </head>
    <body>
        <h1>What do you mean? Játék</h1>

    <div id="wrapper">
        <div id="tables">

            <div class="table-container">
                <p  class="table-title">Rangsor</p>
                <table>
                    <tr>
                        <th>Helyezés</th>
                        <th>Azonosító</th>
                        <th>Szerepkör</th>
                    </tr>
    """

game_page_players_table_close_part = f"""
                </table>
            </div>
        </div>
    """

game_page_right_panel_head_part = f"""
        <div id ="right_panel">
            <details>
                <summary>Aktív játékosok</summary>
    """

game_page_questions_head_part = f"""
                <h2></h2>
            <details>
                <summary>Kérdések az összefoglalóról</summary>
                <div class="questions-container">
    """

game_page_questions_close_part = f"""
                </div>
            </details>
    """

game_page_close_part = f"""
    </div>
    </body>
    </html>
    """
