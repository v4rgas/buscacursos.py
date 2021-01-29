import pandas as pd
import requests


class Curso:
    def __init__(self, sigla):
        self.sigla = sigla

        self.semestres = ['Primer Semestre', 'Segundo Semestre', 'TAV']

        self.url = self._create_url(sigla=self.sigla)
        self.update_table()
        self.current_semester = self.get_current_semester()

    def _create_url(self, sem=[2021, 1], sigla='', nrc='', nombre='', categoria='TODOS', area='TODOS', formato='TODOS', profesor='', campus='TODOS'):
        url = f'http://buscacursos.uc.cl/?cxml_semestre={sem[0]}-{sem[1]}&cxml_sigla={sigla}&cxml_nrc={nrc}&cxml_nombre={nombre}&cxml_categoria={categoria}&cxml_area_fg={area}&cxml_formato_cur={formato}&cxml_profesor={profesor}&cxml_campus={campus}&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS#resultados'
        return url

    def update_table(self):
        url = self.url
        r = requests.get(url)
        df_list = pd.read_html(r.text)
        self.table = df_list
        return df_list

    def get_all_semesters(self):
        table = self.table
        semestres = table[1][1][0]

        for num, semestre in enumerate(self.semestres):
            semestres = semestres.replace(semestre, str(num+1))

        semestres = semestres.split(' ')

        semestres = [[int(semestres[i]), int(semestres[i+1])]
                     for i in range(0, len(semestres)-1, 2)]

        return semestres

    def get_current_semester(self):
        semesters = self.get_all_semesters()
        return semesters[0]

    def secciones(self):
        # print(self.url)
        table = self.table
        try:
            return self.table[5]
        except IndexError:
            return []


if __name__ == "__main__":
    test = Curso('IIC10035')
    print(test.secciones())
