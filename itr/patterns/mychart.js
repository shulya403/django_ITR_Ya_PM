<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        google.charts.load('current', {packages: ['corechart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            // Define the chart to be drawn.
            var data = new google.visualization.DataTable();

            //Data Load

            data.addColumn('date', 'Month');
            {% for ven in  Col %}
                data.addColumn('number', {{ ven }});
            {% endfor %}
            {% for mth, prc in Result_Avg.items %}

                data.addRows([{{ mth|date:"b-y" }}{% for i in prc %},{{ i }}{% endfor %}]);

            {% endfor %}

            var options = {'title':'How Much Pizza I Ate Last Night',
                     'width':400,
                     'height':300};

            //Chart
                var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
                chart.draw(data, null);
        }
    </script>