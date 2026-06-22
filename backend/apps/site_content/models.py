from django.db import models
from solo.models import SingletonModel


class SiteContent(SingletonModel):
    """Editable text for the public home page. Only one row ever exists."""

    historico = models.TextField(
        "Histórico",
        default=(
            "O Torneio Universitário de Atletismo (TUNA) foi criado em 1999 e, "
            "desde então, vem sendo realizado anualmente ao longo de quatro etapas "
            "por ano, envolvendo dezenas de faculdades não só do Estado de São "
            "Paulo, mas também das regiões Sul e Sudeste.\n\n"
            "O nível técnico do TUNA vem aumentando desde sua criação, sem impedir "
            "que atletas iniciantes compitam e ganhem medalhas. Os atletas das "
            "diversas faculdades treinam durante o ano todo para demonstrarem seu "
            "desempenho perante as equipes concorrentes."
        ),
    )
    o_torneio = models.TextField(
        "O Torneio",
        default=(
            "No ano de 2022, o TUNA faz seu retorno após 2 anos de ausência por "
            "conta da pandemia do COVID-19 e suas quatro etapas devem contar com a "
            "participação de mais de 500 atletas de mais de 40 faculdades, sendo "
            "estas em grande parte faculdades de Medicina de todo o Estado de São "
            "Paulo e faculdades da Universidade de São Paulo (USP), além de "
            "convidadas como Escola Naval, Universidade Presbiteriana Mackenzie, "
            "Centro Univertitário Sant'Anna, UNIP, UFPR, entre outras."
        ),
    )
    proxima_etapa = models.TextField(
        "Próxima etapa",
        default=(
            "16/08/2026 - Arena Olímpica - Centro de Atletismo Professor Oswaldo "
            "Terra - R. Tiradentes, 1845 - Santa Terezinha, São Bernardo do "
            "Campo - SP"
        ),
    )
    regulamento_url = models.URLField("Link do regulamento", blank=True)
    contato_email = models.EmailField("E-mail de contato", default="tunaorg@gmail.com")
    instagram_url = models.URLField("Instagram", blank=True)
    facebook_url = models.URLField("Facebook", blank=True)

    class Meta:
        verbose_name = "Conteúdo do site"

    def __str__(self) -> str:
        return "Conteúdo do site"
