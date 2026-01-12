<?php

namespace App\Http\Requests\StudentInfo\ParentGuardian;

use Illuminate\Foundation\Http\FormRequest;

class ParentGuardianUpdateRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, mixed>
     */
    public function rules()
    {
        return [
            // Champs obligatoires (*)
            'guardian_name'          => 'required|max:255',
            'guardian_mobile'        => 'required|max:255|regex:/^[\+\d\s\-\(\)]{10,20}$/|unique:users,phone,'.Request()->user_id,
            'guardian_email'         => 'required|email|max:255|unique:users,email,'.Request()->user_id,
            'father_name'            => 'required|max:255',
            'father_mobile'          => 'required|max:255|regex:/^[\+\d\s\-\(\)]{10,20}$/',
            'mother_name'            => 'required|max:255',
            'mother_mobile'          => 'required|max:255|regex:/^[\+\d\s\-\(\)]{10,20}$/',
            'status'                 => 'required|max:255',
            
            // Champs optionnels
            'father_profession'      => 'nullable|max:255',
            'father_nationality'     => 'nullable|max:255',
            'mother_profession'      => 'nullable|max:255',
            'guardian_profession'    => 'nullable|max:255',
            'guardian_address'       => 'nullable|max:500',
            'guardian_relation'      => 'nullable|max:255',
            'guardian_place_of_work' => 'nullable|max:255',
            'guardian_position'      => 'nullable|max:255',
            
            // Champs système
            'username'               => 'nullable|unique:users,username,'.Request()->user_id.',id',
            
            // Images
            'father_image'           => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
            'mother_image'           => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
            'guardian_image'         => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048'
        ];
    }
}
