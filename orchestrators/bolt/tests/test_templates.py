"""Tests pour les Templates IA Factory"""

import pytest

from src.templates import (
    IAFactoryTemplate,
    TemplateStack,
    IAFACTORY_TEMPLATES,
    list_templates,
    get_template,
    get_template_files,
)


class TestIAFactoryTemplates:
    """Tests des templates IA Factory"""

    def test_templates_defined(self):
        """Test que les templates sont définis"""
        assert len(IAFACTORY_TEMPLATES) == 3

    def test_fastapi_template_exists(self):
        """Test template FastAPI existe"""
        template = get_template("iafactory-fastapi")
        assert template is not None
        assert template.id == "iafactory-fastapi"
        assert template.stack == TemplateStack.FASTAPI

    def test_nextjs_template_exists(self):
        """Test template Next.js existe"""
        template = get_template("iafactory-nextjs")
        assert template is not None
        assert template.id == "iafactory-nextjs"
        assert template.stack == TemplateStack.NEXTJS

    def test_gov_agent_template_exists(self):
        """Test template GOV Agent existe"""
        template = get_template("iafactory-gov-agent")
        assert template is not None
        assert template.id == "iafactory-gov-agent"
        assert template.stack == TemplateStack.PYTHON

    def test_template_not_found(self):
        """Test template non trouvé"""
        template = get_template("nonexistent")
        assert template is None


class TestFastapiTemplate:
    """Tests du template FastAPI"""

    @pytest.fixture
    def template(self):
        return get_template("iafactory-fastapi")

    def test_has_main_file(self, template):
        """Test fichier main.py présent"""
        assert "app/main.py" in template.files

    def test_has_config_file(self, template):
        """Test fichier config.py présent"""
        assert "app/config.py" in template.files

    def test_has_chargily_service(self, template):
        """Test service Chargily présent"""
        assert "app/services/chargily.py" in template.files

    def test_has_requirements(self, template):
        """Test requirements.txt présent"""
        assert "requirements.txt" in template.files

    def test_has_dockerfile(self, template):
        """Test Dockerfile présent"""
        assert "Dockerfile" in template.files

    def test_chargily_code_valid(self, template):
        """Test code Chargily valide"""
        chargily_code = template.files["app/services/chargily.py"]
        assert "ChargilyService" in chargily_code
        assert "CHARGILY_API_KEY" in chargily_code
        assert "create_checkout" in chargily_code
        assert "DZD" in chargily_code

    def test_no_stripe(self, template):
        """Test pas de Stripe"""
        for file_content in template.files.values():
            assert "Stripe" not in file_content or "# NOT Stripe" in file_content

    def test_dependencies(self, template):
        """Test dépendances"""
        assert "fastapi" in template.dependencies
        assert "supabase" in template.dependencies


class TestNextjsTemplate:
    """Tests du template Next.js"""

    @pytest.fixture
    def template(self):
        return get_template("iafactory-nextjs")

    def test_has_layout(self, template):
        """Test layout présent"""
        assert "app/layout.tsx" in template.files

    def test_has_page(self, template):
        """Test page présente"""
        assert "app/page.tsx" in template.files

    def test_has_i18n_config(self, template):
        """Test config i18n présente"""
        assert "i18n.ts" in template.files

    def test_has_middleware(self, template):
        """Test middleware présent"""
        assert "middleware.ts" in template.files

    def test_rtl_support(self, template):
        """Test support RTL"""
        layout_code = template.files["app/layout.tsx"]
        assert "dir=" in layout_code or "rtl" in layout_code.lower()

    def test_languages_supported(self, template):
        """Test langues supportées"""
        i18n_code = template.files["i18n.ts"]
        assert "fr" in i18n_code
        assert "ar" in i18n_code
        assert "en" in i18n_code

    def test_has_package_json(self, template):
        """Test package.json présent"""
        assert "package.json" in template.files


class TestGovAgentTemplate:
    """Tests du template GOV Agent"""

    @pytest.fixture
    def template(self):
        return get_template("iafactory-gov-agent")

    def test_has_main(self, template):
        """Test main.py présent"""
        assert "main.py" in template.files

    def test_has_browser_agent(self, template):
        """Test browser agent présent"""
        assert "agents/browser_agent.py" in template.files

    def test_has_cnas_agent(self, template):
        """Test CNAS agent présent"""
        assert "agents/cnas_agent.py" in template.files

    def test_browser_automation(self, template):
        """Test code automation browser"""
        browser_code = template.files["agents/browser_agent.py"]
        assert "playwright" in browser_code.lower() or "selenium" in browser_code.lower()

    def test_gov_systems_mentioned(self, template):
        """Test systèmes GOV mentionnés"""
        main_code = template.files["main.py"]
        assert "CNAS" in main_code or "gov" in main_code.lower()


class TestListTemplates:
    """Tests de la fonction list_templates"""

    def test_list_templates(self):
        """Test liste des templates"""
        templates = list_templates()
        assert len(templates) == 3
        assert all(isinstance(t, IAFactoryTemplate) for t in templates)

    def test_templates_have_ids(self):
        """Test que tous les templates ont des IDs"""
        templates = list_templates()
        ids = [t.id for t in templates]
        assert "iafactory-fastapi" in ids
        assert "iafactory-nextjs" in ids
        assert "iafactory-gov-agent" in ids


class TestGetTemplateFiles:
    """Tests de la fonction get_template_files"""

    def test_get_fastapi_files(self):
        """Test récupération fichiers FastAPI"""
        files = get_template_files("iafactory-fastapi")
        assert files is not None
        assert "app/main.py" in files

    def test_get_nextjs_files(self):
        """Test récupération fichiers Next.js"""
        files = get_template_files("iafactory-nextjs")
        assert files is not None
        assert "app/layout.tsx" in files

    def test_get_nonexistent_files(self):
        """Test template non existant"""
        files = get_template_files("nonexistent")
        assert files is None


class TestTemplateStack:
    """Tests de l'enum TemplateStack"""

    def test_stack_values(self):
        """Test valeurs des stacks"""
        assert TemplateStack.FASTAPI.value == "fastapi"
        assert TemplateStack.NEXTJS.value == "nextjs"
        assert TemplateStack.REACT.value == "react"
        assert TemplateStack.PYTHON.value == "python"


class TestTemplateModel:
    """Tests du modèle IAFactoryTemplate"""

    def test_template_creation(self):
        """Test création de template"""
        template = IAFactoryTemplate(
            id="test-template",
            name="Test Template",
            description="A test template",
            stack=TemplateStack.PYTHON,
            files={"main.py": "print('hello')"},
            dependencies=["requests"],
            features=["feature1"]
        )
        assert template.id == "test-template"
        assert template.name == "Test Template"
        assert len(template.files) == 1
        assert "requests" in template.dependencies

    def test_template_model_dump(self):
        """Test sérialisation"""
        template = IAFactoryTemplate(
            id="test",
            name="Test",
            description="Test",
            stack=TemplateStack.PYTHON,
            files={},
            dependencies=[],
            features=[]
        )
        data = template.model_dump()
        assert data["id"] == "test"
        assert "stack" in data
