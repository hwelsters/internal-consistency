import xlsxwriter

import datetime

CHATGPT_VERSION = "ChatGPT"

STATS_WORKSHEET_TITLE = 'Overall'
CAUSALITY_WORKSHEET_TITLE = 'Causality_Values'

ADDS_AND_SUBS_TITLE = 'AddsSubs'
MULTS_AND_DIVS_TITLE = 'MultsDivs'
EQUATIONS_TITLE = 'Equations'
UNKNOWNS_TITLE = 'Unknowns'
PAIRS_OF_PARENS_TITLE = 'PairsOfParentheses'
DECIMALS_TITLE = 'Decimals'

CAUSALITY_NAME_COLUMN = "name"
CAUSALITY_SUPPORT_COLUMN = "support"
CAUSALITY_CAUSALITY_COLUMN = "causality"
CAUSALITY_COND_PROB_COLUMN = "conditional_probability"
CAUSALITY_PRIOR_COLUMN = "prior"
CAUSALITY_REL_COLUMN = "rel"

class XlsxWriter:
    @staticmethod
    def write_xlsx(causality_df, output_file_path, label):
        workbook = xlsxwriter.Workbook(output_file_path)

        header_format = workbook.add_format({
            'bold': True, 
            'underline': True,
            'font_size': 20,
            'font_color': 'black',
            'font_name': 'Calibri'})
        
        normal_format = workbook.add_format({
            'font_color': 'black',
            'font_size': 12,
            'font_color': 'black',
            'font_name': 'Calibri',
        })

        border_format = workbook.add_format({
            'font_color': 'black',
            'font_size': 12,
            'font_color': 'black',
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#d3cbbe'
        })
        emphasize_format = workbook.add_format({
            'bold': True, 
            'underline': True,
            'font_color': 'black',
            'font_size': 12,
            'font_color': 'black',
            'font_name': 'Calibri'
        })

        # Causality Values *********************************************************************

        causality_worksheet = workbook.add_worksheet(CAUSALITY_WORKSHEET_TITLE)

        causality_worksheet.set_column(0, 0, 60)

        causality_worksheet.write(1, 0, "Causality Values Chart", header_format)
        causality_worksheet.write(1, 1, CHATGPT_VERSION, header_format)

        causality_worksheet.write(1, 0, "Name", normal_format)
        causality_worksheet.write(1, 1, "Support", normal_format)
        causality_worksheet.write(1, 2, "Quantity", normal_format)
        causality_worksheet.write(1, 3, "Conditional Probability", normal_format)
        causality_worksheet.write(1, 4, "Prior", normal_format)
        causality_worksheet.write(1, 5, "Rel", normal_format)
        causality_worksheet.write(1, 6, "Causality", normal_format)


        index = 0
        for idx, row in causality_df.iterrows():
            causality_worksheet.write(2 + index, 0, row[CAUSALITY_NAME_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 1, row[CAUSALITY_SUPPORT_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 2, index + 1, normal_format)
            causality_worksheet.write(2 + index, 3, row[CAUSALITY_COND_PROB_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 4, row[CAUSALITY_PRIOR_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 5, row[CAUSALITY_REL_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 6, row[CAUSALITY_CAUSALITY_COLUMN], normal_format)
            index += 1

        def make_scattersheet(title, description, starts_with):
            adds_and_subs_worksheet = workbook.add_worksheet(title)
            adds_and_subs_worksheet.set_column(0, 0, 80)
            
            adds_and_subs_df = causality_df.loc[causality_df.apply(lambda row : row[CAUSALITY_NAME_COLUMN].startswith(starts_with), axis=1)]

            adds_and_subs_worksheet.write(0, 0, f"{description} Chart", header_format)
            adds_and_subs_worksheet.write(0, 1, CHATGPT_VERSION, header_format)

            adds_and_subs_worksheet.write(2, 0, "Name", normal_format)
            adds_and_subs_worksheet.write(2, 1, "Support", normal_format)
            adds_and_subs_worksheet.write(2, 2, "Quantity", normal_format)
            adds_and_subs_worksheet.write(2, 3, "Conditional Probability", normal_format)
            adds_and_subs_worksheet.write(2, 4, "Prior", normal_format)
            adds_and_subs_worksheet.write(2, 5, "Conditional - Prior", normal_format)
            adds_and_subs_worksheet.write(2, 6, "Factor 1", normal_format)
            adds_and_subs_worksheet.write(2, 7, "Factor 2", normal_format)
            adds_and_subs_worksheet.write(2, 8, "Square Error", normal_format)
            adds_and_subs_worksheet.write(2, 9, "Confidence Val", normal_format)
            adds_and_subs_worksheet.write(2, 10, "Amount", normal_format)
            adds_and_subs_worksheet.write(2, 11, "Bar", normal_format)

            index = 0
            for idx, row in adds_and_subs_df.iterrows():
                index += 1
                row_index = 2 + index
                excel_index = row_index + 1
                if row[CAUSALITY_COND_PROB_COLUMN] <= 0.001: break

                adds_and_subs_worksheet.write(row_index, 0, row[CAUSALITY_NAME_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 1, row[CAUSALITY_SUPPORT_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 2, index, normal_format)
                adds_and_subs_worksheet.write(row_index, 3, row[CAUSALITY_COND_PROB_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 4, row[CAUSALITY_PRIOR_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 5, row[CAUSALITY_COND_PROB_COLUMN] - row[CAUSALITY_PRIOR_COLUMN], normal_format)
                adds_and_subs_worksheet.write(row_index, 6, f"=1/(POWER(B{excel_index},1.5))", normal_format)
                adds_and_subs_worksheet.write(row_index, 7, f"=SQRT((D{excel_index}-POWER(10,-4))*B{excel_index}*((1-D{excel_index}+POWER(10,-4))*B{excel_index}))", normal_format)
                adds_and_subs_worksheet.write(row_index, 8, f"=G{excel_index}*H{excel_index}", normal_format)
                adds_and_subs_worksheet.write(row_index, 9, 1.95996398454, normal_format)
                adds_and_subs_worksheet.write(row_index, 10, f"=I{excel_index}*J{excel_index}", normal_format)
                adds_and_subs_worksheet.write(row_index, 11, f"=MIN(K{excel_index},1-D{excel_index})", normal_format)


            add_sub_scatter_chart = workbook.add_chart({'type': 'scatter'})
            add_sub_scatter_chart.add_series({
                'categories': f'={title}!$C$4:$C${4 + index}',
                'values': f'={title}!$D$4:$D${4 + index}',
            })
            add_sub_scatter_chart.set_title({'name': description})
            add_sub_scatter_chart.set_x_axis({'name': description, 'name_font': {'size': 24, 'bold': True},})
            add_sub_scatter_chart.set_y_axis({'name': label, 'name_font': {'size': 24, 'bold': True},}) 
            add_sub_scatter_chart.set_size({'width' : 1000, 'height': 1000})
            adds_and_subs_worksheet.insert_chart('M4', add_sub_scatter_chart, {'x_offset': 0, 'y_offset': 0})
        
        make_scattersheet(ADDS_AND_SUBS_TITLE, 'Number of Additions And Subtractions', 'num_of_adds_and_subs')
        make_scattersheet(MULTS_AND_DIVS_TITLE, 'Number of Multiplications And Divisions', 'num_of_mults_and_divs')
        make_scattersheet(EQUATIONS_TITLE, 'Number of Equations', 'num_of_equals')
        make_scattersheet(DECIMALS_TITLE, 'Number of Decimals', 'num_of_decimals')
        make_scattersheet(UNKNOWNS_TITLE, 'Number of Unknowns', 'num_of_unknowns')
        make_scattersheet(PAIRS_OF_PARENS_TITLE, 'Pairs of Parentheses', 'pairs_of_parentheses')

        workbook.close()
        

