package com.anteifilip.appsec.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.anteifilip.appsec.R
import com.anteifilip.appsec.databinding.FragmentAuthBinding
import com.anteifilip.appsec.models.UserBody
import com.anteifilip.appsec.utils.PreferenceHelper
import com.anteifilip.appsec.utils.PreferenceHelper.set
import com.anteifilip.appsec.utils.onClickDebounced
import com.anteifilip.appsec.utils.viewBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

class AuthFragment : Fragment(R.layout.fragment_auth) {

    private val binding by viewBinding(FragmentAuthBinding::bind)
    private val args by navArgs<AuthFragmentArgs>()
    private val viewModel: AppSecViewModel by viewModel()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        observeViewModel()
        initViews()
    }

    private fun observeViewModel() {
        if (args.isLogin) {
            viewModel.loginError.observe(viewLifecycleOwner) {
                Toast.makeText(
                    requireContext(),
                    "Login failed. Please try again.",
                    Toast.LENGTH_SHORT
                ).show()
            }
            viewModel.loginResponse.observe(viewLifecycleOwner) {
                Toast.makeText(
                    requireContext(),
                    "Login success.",
                    Toast.LENGTH_SHORT
                ).show()
                PreferenceHelper.defaultPrefs(requireContext())["userId"] = it
                val intent = Intent(context, PostsActivity::class.java)
                requireActivity().startActivity(intent)
                requireActivity().overridePendingTransition(
                    R.anim.enter_from_right_anim,
                    R.anim.exit_to_left_anim
                )
                requireActivity().finish()
            }
        } else {
            viewModel.userError.observe(viewLifecycleOwner) {
                Toast.makeText(
                    requireContext(),
                    "Registration failed. Please try again.",
                    Toast.LENGTH_SHORT
                ).show()
            }
            viewModel.userResponse.observe(viewLifecycleOwner) {
                Toast.makeText(
                    requireContext(),
                    "Registration success. Please log in.",
                    Toast.LENGTH_SHORT
                ).show()
                findNavController().navigate(AuthFragmentDirections.openAuth(true))
            }
        }
    }

    private fun initViews() = binding.apply {
        authButton.text =
            resources.getString(if (args.isLogin) R.string.login else R.string.register)
        authButton.onClickDebounced {
            if (args.isLogin)
                viewModel.login(
                    UserBody(
                        usernameEditText.text.toString(),
                        passwordEditText.text.toString()
                    )
                )
            else
                viewModel.user(
                    UserBody(
                        usernameEditText.text.toString(),
                        passwordEditText.text.toString()
                    )
                )
        }
    }
}