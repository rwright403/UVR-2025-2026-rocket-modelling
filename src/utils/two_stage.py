from uvicrocketpy import Rocket


class TwoStageRocket:
    
    def _build_stage(self, radius, components, mass_model, drag_model):

        #print("drag_model.power_off: ", drag_model.power_off)

        rocket = Rocket(
            radius=radius,

            mass = mass_model.mass, 
            center_of_mass_without_motor=mass_model.cg[0], 
            inertia = (mass_model.inertia[0][0], mass_model.inertia[1][1], mass_model.inertia[2][2]),  # uvicrocketpy wants a 3-tuple

            power_off_drag = drag_model.power_off,
            power_on_drag = drag_model.power_on,

            coordinate_system_orientation="nose_to_tail",
        )

        for comp in components:
            if comp is None:
                continue  # skip if user left a slot empty

            pos, func = comp
            if func is not None:
                func(rocket, pos)

        return rocket



    def __init__(self,
                s1_rail_buttons,
                s1_diam: float,
                s1_motor_x_pos: float,
                s1_motor,
                s1_fins_x_pos: float,
                s1_fins,
                s1_boattail_x_pos: float,
                s1_boattail,
                s1_mass_model,
                s1_separated_drag_model,
                s1_drogue,
                s1_main,

                full_stack_length: float,
                full_stack_drag_model,

                s2_length: float,
                s2_diam: float,
                s2_motor_x_pos: float, 
                s2_motor, 
                s2_fins_x_pos: float,  
                s2_fins,  
                s2_boattail_x_pos: float, 
                s2_boattail,
                s2_mass_model,
                s2_drag_model,
                s2_drogue,
                s2_main,

                 
                nosecone,
                ):
        

        s1_separated_components = [
            (s1_fins_x_pos, s1_fins),
            (s1_boattail_x_pos, s1_boattail),
            (0, s1_drogue),
            (0, s1_main),
        ]

        full_stack_components = [
            (s1_motor_x_pos, s1_motor),
            (s1_fins_x_pos, s1_fins),
            (s2_fins_x_pos, s2_fins),
            (0, nosecone),
        ]

        s2_components = [
            (s2_motor_x_pos, s2_motor),
            (s2_fins_x_pos, s2_fins),
            (s2_boattail_x_pos, s2_boattail),
            (0, nosecone),
            (0, s2_drogue),
            (0, s2_main),
        ]

        self.stage1_separated = self._build_stage(0.5*s1_diam, s1_separated_components, s1_mass_model, s1_separated_drag_model)
        self.stage1_separated.draw()

        self.stage2 = self._build_stage(0.5*s2_diam, s2_components, s2_mass_model, s2_drag_model)
        self.stage2.draw()

        ### use parallel axis to build full_stack mass model
        full_stack_mass_model = s1_mass_model #mass.parallel_axis( [s1_mass_model, s2_mass_model] )

        self.full_stack = self._build_stage(0.5*s1_diam, full_stack_components, full_stack_mass_model, full_stack_drag_model)

        self.full_stack.set_rail_buttons(*s1_rail_buttons)
        self.full_stack.draw()


"""
        if self.stage2.radius != self.full_stack.radius:
            self.full_stack.add_tail(
                top_radius = self.stage2.radius, 
                bottom_radius = self.full_stack.radius, 
                length = 0.1*(full_stack_length - s2_length), #TODO:
                position = s2_length #TODO: check this
            )"""
