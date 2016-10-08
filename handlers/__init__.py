from monk.handler import MonkRegister
from handlers.epocacosmeticos_handler import EpocaCosmeticosHandler
from handlers.bloghenriquelopes_handler import BlogHenriqueLopesHandler

MonkRegister\
    .add(EpocaCosmeticosHandler)\
    .add(BlogHenriqueLopesHandler, disabled=True)
