from agents.crud.generators.backend.root.main_generator import MainGenerator
from agents.crud.generators.backend.database_init_generator import DatabaseInitGenerator
from agents.crud.generators.backend.controller_generator import ControllerGenerator
from agents.crud.generators.backend.dto_generator import DtoGenerator
from agents.crud.generators.backend.create_dto_generator import CreateDtoGenerator
from agents.crud.generators.backend.update_dto_generator import UpdateDtoGenerator
from agents.crud.generators.backend.response_dto_generator import ResponseDtoGenerator
from agents.crud.generators.backend.database_generator import DatabaseGenerator
from agents.crud.generators.backend.model_generator import ModelGenerator
from agents.crud.generators.backend.repository_generator import RepositoryGenerator
from agents.crud.generators.backend.route_generator import RouteGenerator
from agents.crud.generators.backend.schema_generator import SchemaGenerator
from agents.crud.generators.backend.service_generator import ServiceGenerator
from agents.crud.generators.backend.validator_generator import ValidatorGenerator

from agents.crud.generators.database.sql_generator import SqlGenerator


# FRONTEND TYPES
from agents.crud.generators.frontend.types.entity_type_generator import EntityTypeGenerator
from agents.crud.generators.frontend.types.create_type_generator import CreateTypeGenerator
from agents.crud.generators.frontend.types.update_type_generator import UpdateTypeGenerator
from agents.crud.generators.frontend.types.response_type_generator import ResponseTypeGenerator
from agents.crud.generators.frontend.types.filter_type_generator import FilterTypeGenerator
from agents.crud.generators.frontend.types.index_type_generator import IndexTypeGenerator


# FRONTEND API
from agents.crud.generators.frontend.api.api_generator import ApiGenerator
from agents.crud.generators.frontend.api.service_generator import ServiceGenerator as FrontendServiceGenerator


# FRONTEND HOOK
from agents.crud.generators.frontend.hooks.hook_generator import HookGenerator


# FRONTEND COMPONENTS
from agents.crud.generators.frontend.components.table_generator import TableGenerator
from agents.crud.generators.frontend.components.form_generator import FormGenerator
from agents.crud.generators.frontend.components.modal_generator import ModalGenerator
from agents.crud.generators.frontend.components.toolbar_generator import ToolbarGenerator
from agents.crud.generators.frontend.components.filter_generator import FilterGenerator


# FRONTEND PAGES
from agents.crud.generators.frontend.pages.page_generator import PageGenerator
from agents.crud.generators.frontend.routes.route_generator import RouteGenerator as FrontendRouteGenerator
from agents.crud.generators.frontend.index.index_generator import IndexGenerator


# ROOT
from agents.crud.generators.frontend.root.root_route_generator import RootRouteGenerator
from agents.crud.generators.frontend.root.home.home_generator import HomeGenerator
from agents.crud.generators.frontend.root.app.app_generator import AppGenerator


class GeneratorRegistry:
    """
    Registro central de todos los generadores.
    """

    def __init__(self):

        self._generators = []


        # ===========================
        # BACKEND
        # ===========================

        self.register(ModelGenerator())
        self.register(SchemaGenerator())
        self.register(DtoGenerator())
        self.register(CreateDtoGenerator())
        self.register(UpdateDtoGenerator())
        self.register(ResponseDtoGenerator())
        self.register(ValidatorGenerator())
        self.register(RepositoryGenerator())
        self.register(ServiceGenerator())
        self.register(ControllerGenerator())
        self.register(RouteGenerator())
        self.register(MainGenerator())
        self.register(DatabaseInitGenerator())

        # ===========================
        # DATABASE
        # ===========================

        self.register(DatabaseGenerator())
        self.register(SqlGenerator())


        # ===========================
        # FRONTEND TYPES
        # ===========================

        self.register(EntityTypeGenerator())
        self.register(CreateTypeGenerator())
        self.register(UpdateTypeGenerator())
        self.register(ResponseTypeGenerator())
        self.register(FilterTypeGenerator())
        self.register(IndexTypeGenerator())


        # ===========================
        # FRONTEND API
        # ===========================

        self.register(ApiGenerator())
        self.register(FrontendServiceGenerator())


        # ===========================
        # FRONTEND HOOK
        # ===========================

        self.register(HookGenerator())


        # ===========================
        # FRONTEND COMPONENTS
        # ===========================

        self.register(TableGenerator())
        self.register(FormGenerator())
        self.register(ModalGenerator())
        self.register(ToolbarGenerator())
        self.register(FilterGenerator())


        # ===========================
        # FRONTEND PAGES
        # ===========================

        self.register(PageGenerator())
        self.register(FrontendRouteGenerator())
        self.register(IndexGenerator())


        # ===========================
        # ROOT
        # ===========================

        self.register(HomeGenerator())
        self.register(RootRouteGenerator())
        self.register(AppGenerator())


    def register(self, generator):

        self._generators.append(generator)


    def all(self):

        return sorted(
            self._generators,
            key=lambda g: g.order,
        )


    def get(self, name: str):

        for generator in self._generators:

            if generator.name == name:
                return generator

        return None
