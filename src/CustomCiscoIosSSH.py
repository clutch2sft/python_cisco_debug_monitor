from netmiko.cisco.cisco_ios import CiscoIosSSH

# class CustomCiscoIosSSH(CiscoIosSSH):
#     def session_preparation(self):
#         """
#         Prepare the session after the connection has been established but modify the order.
#         Customize to handle unique enable prompt pattern.
#         """
#         self.set_base_prompt()
#         # Use a custom regex pattern that matches the expected enable prompt
#         #custom_enable_pattern = r'AP[A-F0-9]{4}\.[A-F0-9]{4}\.[A-F0-9]{4}#'
#         #self.enable(pattern=custom_enable_pattern)
#         self.enable()
#         self.disable_paging(command="terminal length 0")
#         self.set_terminal_width(command="terminal width 132")


# class CustomCiscoIosSSH(CiscoIosSSH):
#     def enable(self, *args, **kwargs):
#         """Override enable to use regex pattern for prompt detection."""
#         pattern = r'AP[A-Fa-f0-9]{4}\.[A-Fa-f0-9]{4}\.[A-Fa-f0-9]{4}#[A-Fa-f0-9]{4}#'
#         return super().enable(*args, pattern=pattern, **kwargs)

#     def session_preparation(self):
#         self.set_base_prompt()
#         self.enable()  # Using overridden method with regex support
#         self.disable_paging(command="terminal length 0")
#         self.set_terminal_width(command="terminal width 132")


# class CustomCiscoIosSSH(CiscoIosSSH):
#     def session_preparation(self):
#         """
#         Prepare the session after the connection has been established.
#         This includes setting the base prompt and ensuring that different prompts
#         are handled correctly for regular and enable modes.
#         """
#         pass
        # Set the base prompt to handle the initial connection, which might end with '>'
        # base_prompt = self.find_prompt(delay_factor=2)
        # if '>' in base_prompt:
        #     # If the base prompt ends with '>', we need to handle it for regular mode
        #     self.set_base_prompt()

        # Use the enable() function to switch to privileged mode, which should end with '#'
        # self.enable()  # You can add expect_string='#' if the default isn't working
        
        # # Once in privileged mode, set terminal settings
        # self.disable_paging(command="terminal length 0")
        # self.set_terminal_width(command="terminal width 132")

class CustomCiscoIosSSH(CiscoIosSSH):
    def session_preparation(self):
        """Prepare the session after the connection has been established but modify the order."""
        self.set_base_prompt()
        self.enable()  # Ensure enable mode is activated first.
        self.disable_paging(command="terminal length 0")  # Adjust the command as needed.
        self.set_terminal_width(command="terminal width 132")