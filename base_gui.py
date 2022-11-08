from typing import TypeVar, Tuple, List, Dict, Optional, Any, Union
import pygame
pygame.init()

TupleBoolean = TypeVar('tuple[fit to x: Bool, fit to y: Bool]')
pyg_suf = TypeVar('Surface')
wind = TypeVar('Optional[Surface]')
Frame = TypeVar('Frame')
Rect = TypeVar('Rect')
Anchor = TypeVar('Anchor[str] (eg. topright, center, midtop, ...)')
BaseSprite = TypeVar('Sprite')
btp_note = TypeVar('Note: If enabled, always put this frame before the parent')
AnyData = TypeVar('Function | Object | str, bool, list | etc.')
NON_CALLABLE = TypeVar('NonCallable')

def blit_sprites(sprites):
    """A good built in sprite renderer for this module"""
    for a_ in sprites:
        a_.update()
        rect__ = a_.rect
        if hasattr(a_, "ext_mode"):
            ext_anchor = getattr(a_.rect, a_.ext_anchor)
            for i in a_.b_suf:
                if i:
                    new_anch = (ext_anchor[0] - getattr(i.get_rect(), a_.ext_anchor)[0],
                                ext_anchor[1] - getattr(i.get_rect(), a_.ext_anchor)[1])
                    a_.blit_to.blit(i, new_anch)
        a_.blit_to.blit(a_.image, a_.rect)
        if hasattr(a_, "ext_mode"):
            for i in a_.f_suf:
                if i:
                    aaa = (0, 0, i.get_width(), i.get_height())
                    if isinstance(a_, TextBox) and a_.image.get_width() < i.get_width():
                        aaa = (i.get_width() - a_.image.get_width(), 0, a_.image.get_width(), rect__[3])
                    new_anch = (ext_anchor[0] - getattr(i.get_rect(), a_.ext_anchor)[0] + (aaa[0] / 2),
                                ext_anchor[1] - getattr(i.get_rect(), a_.ext_anchor)[1])
                    a_.blit_to.blit(i, new_anch, aaa)
def blit_groups(groups):
    for group in groups:
        blit_sprites(group)
class BaseButton:
    """**YOU CANNOT CALL THIS CLASS**"""
    def on_clicked(self):
        if callable(self.function):
            if self.args == -1013: return self.function()
            return self.function(self.args)
        return self.function
    def get_if_clicked(self, mouse_pos):
        if self.rect.right >= mouse_pos[0] >= self.rect.left and self.rect.bottom >= mouse_pos[1] >= self.rect.top:
            return True
        return False
    def run_when_clicked(self, mouse_pos):
        if self.get_if_clicked(mouse_pos):
            self.pressed=True; return self.on_clicked()
        self.pressed=False; return None
class BasicFrame:
    """
    Create simple Frame for pygame
    """

    def __init__(self, pos:Tuple, size:Tuple, color:Tuple, anchor="topleft", scale_to_parent=(False, False),
                 ratio_by_parent=False, parent:Optional[BaseSprite]=None, blit_as_local_to_parent=False):
        """
        **Note:** Put this frame before the parent if **blit_as_local_to_parent** is **Enabled**
        """
        self.last_window_size_ = None
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.color = color
        self.image.fill(color)
        self.anchor = anchor
        self.fit_scale = scale_to_parent
        self.ratio_enabled = ratio_by_parent
        self.blit_parent_mode = blit_as_local_to_parent
        self.offset = pos
        self.parent_obj = parent
        self.enabled = True
        if not parent: self.parent = {"surface":pygame.display.get_surface(), "rect":pygame.display.get_surface().get_rect()}
        else: self.parent = {"surface":parent.image, "rect":parent.rect}
        if blit_as_local_to_parent: self.blit_to = parent.image
        else: self.blit_to = pygame.display.get_surface()
        ##################################
        self.fix_everything()
    def fix_everything(self):
        self.fit_to_scale(self.fit_scale)
        if self.ratio_enabled:
            self.ratio_scale_from_parent()
        self.anchor_to_parent(self.anchor)
    def fit_to_scale(self, scale:TupleBoolean, parent:pyg_suf=None):
        """Fit Frame to parent"""
        if not parent: parent = self.parent
        fitting_size = list(self.rect.size)
        if scale[0]:
            fitting_size[0] = parent['surface'].get_width()
        if scale[1]:
            fitting_size[1] = parent['surface'].get_height()
        self.rect.size = fitting_size
        self.image = pygame.transform.scale(self.image, self.rect.size)
    def ratio_scale_from_parent(self, parent:pyg_suf=None):
        """Ratio Frame to parent with its current size"""
        if not parent: parent = self.parent
        p_size = parent['surface'].get_size()
        r_left = self.rect.h / self.rect.w
        r_right = p_size[1] / p_size[0]
        if r_right > r_left:
            self.rect.w = p_size[0]
            self.rect.h = round(p_size[0] * r_left)
        else:
            self.rect.h = p_size[1]
            self.rect.w = round(p_size[1] / r_left)
        self.image = pygame.transform.scale(self.image, self.rect.size)
    def anchor_to_parent(self, anchor:Anchor, parent:pyg_suf=None):
        """Change the anchor of Frame to parent"""
        if not parent: parent = self.parent
        setattr(self.rect, anchor, getattr(parent['rect'], anchor))  # returns 0, 0 bc surface, need find offset
        self.rect.left += self.offset[0]
        self.rect.top += self.offset[1]
    def update(self):
        """
        Update definitions of Frame;
        Includes: update Frame after resize window, update rect of parent for functions in this frame
        """
        # update rect #
        if self.parent_obj: self.parent['rect'] = self.parent_obj.rect
        else: self.parent['rect'] = pygame.display.get_surface().get_rect()
        if self.blit_parent_mode: self.image.fill(self.color)
        if not self.last_window_size_ or self.last_window_size_ != pygame.display.get_window_size(): # if window resized
            self.last_window_size_ = pygame.display.get_window_size()
            self.fit_to_scale(self.fit_scale)
            if self.ratio_enabled: self.ratio_scale_from_parent()
            self.anchor_to_parent(self.anchor)
class AdvancedFrame(BasicFrame):
    """Create an Advanced Frame for pygame"""
    def __init__(self, *args, f_surfaces=None, b_surfaces=None, ext_anchor="topleft", **kwargs):
        """
        Create an Advanced Frame for pygame

        :param f_surfaces: images on front of Frame
        :param b_surfaces: images on back of Frame
        :param ext_anchor: anchor of the image in the ext_surfaces
        """
        super(AdvancedFrame, self).__init__(*args, **kwargs)
        if b_surfaces is None:
            b_surfaces = []
        if f_surfaces is None:
            f_surfaces = []
        self.ext_mode = True
        self.f_suf = f_surfaces
        self.b_suf = b_surfaces
        self.ext_anchor = ext_anchor
class ImageFrame(BasicFrame):
    """Create an Image Frame"""
    def __init__(self, image, *args, **kwargs):
        """
        Create an Image Frame

        :param image: The image for this frame
        """
        super(ImageFrame, self).__init__(*args, **kwargs)
        self.image = image
class ImageButton(ImageFrame, BaseButton):
    def __init__(self, function:AnyData, *args, function_args=-1013, **kwargs):
        f"""
        Create a Image Button \n
        **Note:** If you can only pass **function_args** if **function** is a function **itself**
        """
        super(ImageButton, self).__init__(*args, **kwargs)
        self.function = function
        self.args = function_args
        self.pressed = False
class AdvancedImageButton(ImageButton):
    """Create an Advance Image Button"""
    def __init__(self, *args, f_surfaces=None, b_surfaces=None, ext_anchor="topleft", **kwargs):
        super(AdvancedImageButton, self).__init__(*args, **kwargs)
        if b_surfaces is None:
            b_surfaces = []
        if f_surfaces is None:
            f_surfaces = []
        self.ext_mode = True
        self.f_suf = f_surfaces
        self.b_suf = b_surfaces
        self.ext_anchor = ext_anchor
class TextFrame(AdvancedFrame):
    """Create a Text Frame"""
    def __init__(self, text, font, font_size, *args, background=None, antialias=True, text_color=(0, 0, 0), text_fit=False, text_alignment="center",**kwargs):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(font, font_size)
        self.antialias = antialias
        self.text_color = text_color
        self.background = background
        self.text_fit = text_fit
        ########################
        super(TextFrame, self).__init__(*args, **kwargs)
        self.f_suf = [self.font.render(self.text, antialias, text_color)]
        self.ext_anchor = text_alignment
        self.image = pygame.Surface(args[1])
        self.image.set_alpha(0)
        if background:
            self.image.fill(background)
            self.image.set_alpha(255)
class TextButton(TextFrame, BaseButton):
    """Create a Text Button"""
    def __init__(self, function:AnyData, *args, function_args=-1013, **kwargs):
        f"""
        Create a Text Button \n
        **Note:** If you can only pass **function_args** if **function** is a function **itself**
        """
        super(TextButton, self).__init__(*args, **kwargs)
        self.function = function
        self.args = function_args
        self.pressed = False
class TextBox(TextFrame):
    """Create a TextBox that you can type with it"""
    def __init__(self, *args, shadow_text_color=(50, 50, 50), typing_indicator="Type here",**kwargs):
        """To access text in the TextBox, you need to get the text of this object (ex. theText = TextBox.Text)"""
        args = list(args)
        args.insert(0, typing_indicator)
        if not 'background' in kwargs:
            kwargs['background'] = (255, 255, 255)
        super(TextBox, self).__init__(*args, **kwargs)
        self.original_text_color = self.text_color
        self.text_color = shadow_text_color
        self.on_typing = False
        self.content_added = False
        self.typing_ind = typing_indicator
    def run_when_clicked(self, mouse_pos):
        self.on_typing = self.get_if_clicked(mouse_pos)
    def get_if_clicked(self, mouse_pos):
        if self.rect.right >= mouse_pos[0] >= self.rect.left and self.rect.bottom >= mouse_pos[1] >= self.rect.top:
            self.f_suf[0] = self.font.render(self.text, self.antialias, self.text_color)
            self.image.set_alpha(200)
            self.fix_everything()
            return True
        self.f_suf[0] = self.font.render(self.text, self.antialias, self.original_text_color)
        self.image.set_alpha(255)
        self.fix_everything()
        return False
    def type(self, key):
        f"""
        Type text handler. Will type text if on_typing = True \n
        :return: finished_typing (bool)
        """
        if not self.on_typing or not key: return
        finished_typing = False
        if not self.content_added:
            self.text = ""
            self.content_added = True
        if key.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            if len(self.text) == 0:
                self.content_added = False,
                self.text = self.typing_ind
        elif key.key == pygame.K_RETURN:
            self.on_typing = False
            self.f_suf[0] = self.font.render(self.text, self.antialias, self.original_text_color)
            self.image.set_alpha(255)
            self.fix_everything()
            finished_typing = True
        else:
            self.text = self.text + key.unicode
        self.f_suf[0] = self.font.render(self.text, self.antialias, self.original_text_color)
        self.fix_everything()
        return finished_typing

#################### delete unnecessary junk #####################
del TupleBoolean, pyg_suf, wind, Frame, Rect, Anchor, BaseSprite, AnyData